from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import json
import stripe
from .models import Category, SubCategory, Product, ProductReview, Cart, CartItem, Order, Favorite
from .serializers import (
    UserSerializer, UserLoginSerializer, CategorySerializer, SubCategorySerializer,
    ProductSerializer, ProductReviewSerializer, CartSerializer, OrderSerializer,
    CategoryWithDetailsSerializer, FavoriteSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginUserView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class PublicCategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Категория не найдена"}, status=404)
        serializer = CategoryWithDetailsSerializer(category)
        return Response(serializer.data)

class SubCategoryListView(APIView):
    def get(self, request):
        category_id = request.GET.get('category_id')
        if category_id:
            subcategories = SubCategory.objects.filter(category_id=category_id)
        else:
            subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=404)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductReviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=404)
        review = ProductReview(
            product=product,
            user=request.user,
            rating=request.data['rating'],
            review_text=request.data['review_text']
        )
        review.save()
        return Response(ProductReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    def get(self, request, product_id):
        reviews = ProductReview.objects.filter(product__id=product_id)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            print("Cart data:", serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print("Error in CartView.get:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Товар удалён из корзины'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.cartitem_set.exists():
                print("Cart is empty")
                return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
            # Создаем заказ с начальным статусом
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                status='Pending',
                payment_status='Pending'
            )
            # НЕ очищаем корзину здесь
            print(f"Order created: {order.id} for user: {request.user.username}")
            return Response(
                {'order_id': order.id, **OrderSerializer(order).data},
                status=status.HTTP_201_CREATED
            )
        except Cart.DoesNotExist:
            print("Cart not found")
            return Response({'error': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in OrderListView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({"categories": [], "products": []})

        categories = Category.objects.filter(name__icontains=query)
        category_serializer = CategorySerializer(categories, many=True)
        products = Product.objects.filter(title__icontains=query)
        product_serializer = ProductSerializer(products, many=True)

        return Response({
            "categories": category_serializer.data,
            "products": product_serializer.data
        })

class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получить список избранных продуктов пользователя"""
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Добавить продукт в избранное"""
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            if created:
                return Response({'message': 'Продукт добавлен в избранное'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        """Удалить продукт из избранного"""
        try:
            favorite = Favorite.objects.get(user=request.user, product__id=product_id)
            favorite.delete()
            return Response({'message': 'Продукт удалён из избранного'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'error': 'Продукт не найден в избранном'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request):
        try:
            print(f"Request body: {request.body}")
            data = json.loads(request.body)
            username = data.get('username')
            order_id = data.get('order_id')

            if not username:
                print("Username is missing")
                return JsonResponse({'error': 'Username is required'}, status=400)
            if not order_id:
                print("Order ID is missing")
                return JsonResponse({'error': 'Order ID is required'}, status=400)

            try:
                user = User.objects.get(username=username)
                print(f"Found user: {user.username}")
            except User.DoesNotExist:
                print(f"User {username} not found")
                return JsonResponse({'error': 'User not found'}, status=404)

            try:
                order = Order.objects.get(id=order_id, user=user)
                print(f"Found order: {order.id} for user: {user.username}")
            except Order.DoesNotExist:
                print(f"Order {order_id} not found or not authorized for user: {username}")
                return JsonResponse({'error': 'Order not found or not authorized'}, status=404)

            cart = order.cart
            line_items = []

            cart_items = cart.cartitem_set.all()
            print(f"Cart items: {[item.product.title for item in cart_items]}")
            if not cart_items.exists():
                print("Cart is empty")
                return JsonResponse({'error': 'Cart is empty'}, status=400)

            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'kzt',
                        'product_data': {'name': item.product.title},
                        'unit_amount': int(float(item.product.price)*100),  # Учитываем строковую цену
                    },
                    'quantity': item.quantity,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.DOMAIN + '/success?order_id=' + str(order_id),
                cancel_url=settings.DOMAIN + '/cancel',
                metadata={'order_id': str(order_id)},
            )
            print(f"Checkout session created: {session.url}")
            return JsonResponse({'checkout_url': session.url})
        except Exception as e:
            print(f"Error in CreateCheckoutSessionView: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Signature verification failed: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.payment_id = session['id']
                order.payment_status = 'Completed'
                order.status = 'Shipped'
                order.save()
                # Очищаем корзину
                CartItem.objects.filter(cart=order.cart).delete()
                print(f"✅ Order {order_id} updated: Payment {session['id']} completed, cart cleared")
            except Order.DoesNotExist:
                print(f"Order {order_id} not found")
                return HttpResponse(status=404)
    return HttpResponse(status=200)



class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден или не принадлежит пользователю'}, status=status.HTTP_404_NOT_FOUND)
