from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    phone       = models.CharField(max_length=20)
    address     = models.CharField(max_length=255, blank=True)
    status      = models.CharField(max_length=20, default='new')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products    = models.ManyToManyField(Product, through='OrderItem')

    def __str__(self):
        return f"Заказ {self.id}"

class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Banner(models.Model):
    title = models.CharField("Заголовок (необязательно)", max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    order = models.PositiveIntegerField(
        "Порядок", default=0,
        help_text="Чем меньше — тем раньше в карусели"
    )
    active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Banner {self.id}"