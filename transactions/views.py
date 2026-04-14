from google import genai
from openai import OpenAI
from django.conf import settings
from rest_framework import viewsets
from django.db.models import F, Sum
from .filters import TransactionFilter
from .models import Category, Transaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, TransactionSerializer

# OpenAI client initialization
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Gemini client initialization
if settings.GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

# CategoryViewSet for managing categories
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# TransactionViewSet for managing transactions
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related('category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ViewSet for calculating transaction summary
class TransactionSummaryViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        summary = (
            transactions
            .values('category__name', transaction_type=F('type'))
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        return Response({
            'message': 'Successfully calculated summary',
            'data': {
                'user': request.user.username,
                'summary': summary
            }
        })


# ViewSet for calculating total transaction amount
class TransactionTotalViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total income and expense',
            'data':{
                'user': request.user.username,
                'transaction_count': transactions.count(),
                'total': total
                }})


# ViewSet for calculating total income
class TotalIncomeViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user, type='income')
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total income',
            'data': {
                'user': request.user.username,
                'total_income': total
            }
        })


# ViewSet for calculating total expense
class TotalExpenseViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user, type='expense')
        total = transactions.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'message': 'Successfully calculated total expense',
            'data': {
                'user': request.user.username,
                'total_expense': total
            }
        })


# ViewSet for calculating net balance
class NetBalanceViewSet(viewsets.ViewSet):
    permission_class = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        net_balance = total_income - total_expense
        if net_balance >= 0:
            balance_status = 'Cheers! You are in surplus.'
        else:
            balance_status = 'Oops! You are in debt.'

        return Response({
            'message': 'Successfully calculated net balance',
            'data': {
                'user': request.user.username,
                'net_balance': net_balance,
                'balance_status': balance_status
            }
        })
    

# InsightViewSet for generating financial insights using OpenAI and Gemini
class TransactionsInsightView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        if not transactions.exists():
            return Response({
                'message': 'No transactions found for the user.',
                'data': {
                    'user': request.user.username,
                    'insights': 'No transactions available to generate insights.'
                }
            })
        
        total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        top_category = (
            transactions.values('category__name', transaction_type=F('type'))
            .annotate(total=Sum('amount'))
            .order_by('-total')
            .first()
        )

        prompt = f"""
        User financial summary:
        - Total income: {total_income}
        - Total expense: {total_expense}
        - Top earning/spending category: {top_category['category__name'] if top_category else 'N/A'}

        Give a short, two-line financial insight.
        """

        insight = None
        top_category_name = top_category['category__name'] if top_category else 'N/A'

        # --- 1. Try OpenAI ---
        try:
            openai_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
            )
            openai_text = getattr(openai_response.choices[0].message, "content", None)
            if openai_text:
                insight = openai_text.strip()
        except Exception:
            insight = None

        # --- 2. Try Gemini only if OpenAI did not return a result ---
        if insight is None and settings.GEMINI_API_KEY:
            try:
                gemini_response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                )
                gemini_text = None

                if getattr(gemini_response, "text", None):
                    gemini_text = gemini_response.text

                elif getattr(gemini_response, "candidates", None):
                    first_candidate = gemini_response.candidates[0]
                    content = getattr(first_candidate, "content", None)

                    if content and getattr(content, "parts", None):
                        gemini_text = "".join(
                            [getattr(part, "text", "") or "" for part in content.parts]
                        ).strip()

                if gemini_text:
                    insight = gemini_text

            except Exception:
                insight = None

        # --- 3. Fallback ---
        if not insight:
            if total_expense > total_income:
                insight = f"You are overspending, mainly on {top_category_name}."

            else:
                insight = f"Your spending is under control, mostly in {top_category_name}."

        return Response({
            'message': 'Successfully generated financial insights',
            'data': {
                'user': request.user.username,
                'total_income': total_income,
                'total_expense': total_expense,
                'insights': insight
            }   
        })
