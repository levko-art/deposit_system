# Generated by Django 2.2.20 on 2021-05-11 18:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import exchange.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exchange', '0080_currency_currency_scale'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, 'Deposit wallet'), (1, 'Reward wallet')])),
                ('balance', exchange.fields.FixedDecimalField(default=0.0, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('treasury_id', models.IntegerField(null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=128)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('emit_duration', models.DurationField(blank=True, null=True)),
                ('begin_date', models.DateTimeField(blank=True, null=True)),
                ('prestake_date', models.DateTimeField(blank=True, help_text='Date of prestake opens', null=True)),
                ('iteration', models.DurationField(default={'hours': 1})),
                ('is_enable', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=False)),
                ('last_rewarded', models.DateTimeField(blank=True, null=True)),
                ('claim_enabled', models.BooleanField(default=False)),
                ('stack_enabled', models.BooleanField(default=False)),
                ('unstack_enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('hyperlink', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, 'Deposit wallet'), (1, 'Reward wallet')])),
                ('balance', exchange.fields.FixedDecimalField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', exchange.fields.FixedDecimalField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(0, 'Stack'), (1, 'Unstack')])),
                ('status', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Pending'), (2, 'Success'), (3, 'Failed')], default=0)),
                ('rewarded', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Account')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Wallet')),
            ],
            options={
                'ordering': ['-created_at', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', exchange.fields.FixedDecimalField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', 'id'],
            },
        ),
        migrations.AddField(
            model_name='program',
            name='links',
            field=models.ManyToManyField(blank=True, to='blockfarm.ProgramLink'),
        ),
        migrations.AddField(
            model_name='program',
            name='reward_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency'),
        ),
        migrations.AddField(
            model_name='program',
            name='transaction_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency'),
        ),
        migrations.CreateModel(
            name='ClaimReward',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', exchange.fields.FixedDecimalField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('status', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Pending'), (2, 'Success'), (3, 'Failed')], default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(help_text='Program Account with all Rewards', on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Account')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='exchange.Currency')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(help_text='Link to wallet with user wallet for Reward currency', on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Wallet')),
            ],
            options={
                'ordering': ['-created_at', 'id'],
            },
        ),
        migrations.AddField(
            model_name='account',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blockfarm.Program'),
        ),
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.CheckConstraint(check=models.Q(balance__gte=0), name='balance_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.UniqueConstraint(fields=('type', 'user', 'program'), name='unique_wallet'),
        ),
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='reward',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='claimreward',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(fields=('type', 'program'), name='unique_account'),
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.CheckConstraint(check=models.Q(balance__gte=0), name='balance_gte_0'),
        ),
    ]
