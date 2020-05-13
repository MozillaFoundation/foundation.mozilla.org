# [2020-05-11] Custom Django 2.2.12 migration for handling superclass model renaming.

from django.db import migrations, models
import django.db.models.deletion

from ..utils import AlterModelBases


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0048_auto_20200507_1619'),
    ]

    operations = [
        # Step 1: rename the parent links in our subclasses to match their future name:

        migrations.RenameField(model_name='generalproduct', old_name='baseproduct_ptr', new_name='product_ptr',),
        migrations.RenameField(model_name='softwareproduct', old_name='baseproduct_ptr', new_name='product_ptr',),

        # Step 2: then, temporarily set the base model for our subclassses to just `Model`, which makes Django
        #         think there are no parent links, which mean it won't try to apply crashing logic in step 3.

        AlterModelBases("GeneralProduct", (models.Model,)),
        AlterModelBases("SoftwareProduct", (models.Model,)),

        # Step 3: Now we can safely rename the superclass without Django trying solve subclass pointers:

        migrations.RenameModel(old_name="BaseProduct", new_name="Product"),

        # Step 4: Which means we can now update the `parent_link` fields for the subclasses. Even though we
        #         altered the model bases earlier, this step will restore the class hierarchy:

        migrations.AlterField(
            model_name='generalproduct',
            name='product_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True, primary_key=True,
                serialize=False,
                to='buyersguide.Product'
            ),
        ),
        migrations.AlterField(
            model_name='softwareproduct',
            name='product_ptr',
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to='buyersguide.Product'
            ),
        ),

        # And of course in our case, also make sure the voting models point
        # to the new Product class instead of the old BaseProduct class.
        migrations.AlterField(
            model_name='booleanvote',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyersguide.Product'),
        ),
        migrations.AlterField(
            model_name='booleanproductvote',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_product_votes', to='buyersguide.Product'),
        ),
        migrations.AlterField(
            model_name='rangevote',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyersguide.Product'),
        ),
        migrations.AlterField(
            model_name='rangeproductvote',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='range_product_votes', to='buyersguide.Product'),
        ),
    ]
