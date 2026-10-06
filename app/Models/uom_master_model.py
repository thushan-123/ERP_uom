from django.db import models
from django.conf import settings

class uom_master(models.Model):
    uom_id = models.BigAutoField(primary_key=True)
    uom_code = models.CharField(max_length=20, unique=True)
    uom_name = models.CharField(max_length=100)
    uom_category = models.CharField(max_length=30)
    decimal_places = models.PositiveIntegerField(default=0)
    description = models.CharField( max_length=250, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uom_created"
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uom_modified"
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    # created_by_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='uom_created')
    # modified_at = models.DateTimeField(auto_now=True)
    # modified_by_id = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ref_item_uom_master'
        ordering = ['uom_code']

    def __str__(self):
        return f"{self.uom_code} - {self.uom_name}"