# Generated by Django 4.2.6 on 2023-11-18 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('ActividadID', models.AutoField(primary_key=True, serialize=False)),
                ('Descripcion', models.TextField()),
                ('ValorTotal', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
                'ordering': ['ActividadID'],
            },
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('EventoID', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=255)),
                ('Descripcion', models.TextField(blank=True, null=True)),
                ('Tipo', models.CharField(choices=[('viaje', 'Viaje'), ('hogar', 'Hogar'), ('pareja', 'Pareja'), ('comida', 'Comida'), ('otro', 'Otro')], default='otro', max_length=10)),
                ('FotoOAvatar', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['EventoID'],
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=400, null=True)),
                ('FotoOAvatar', models.CharField(choices=[('https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', 'avatar 1'), ('https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png', 'avatar 2'), ('https://cdn3.iconfinder.com/data/icons/business-avatar-1/512/11_avatar-512.png', 'avatar 3'), ('https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', 'avatar 4'), ('https://as1.ftcdn.net/v2/jpg/01/21/93/74/1000_F_121937450_E3o8jRG3mKbMaAFprSuNOlyrLraSVVua.jpg', 'avatar 5'), ('https://banner2.cleanpng.com/20180625/req/kisspng-computer-icons-avatar-business-computer-software-user-avatar-5b3097fcae25c3.3909949015299112927133.jpg', 'avatar 6')], default='https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Perfil', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Saldos',
            fields=[
                ('SaldoID', models.AutoField(primary_key=True, serialize=False)),
                ('TotalDeuda', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TotalPago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Apodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Saldo_para', to='api.perfil', to_field='user')),
                ('EventoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.eventos')),
            ],
            options={
                'verbose_name': 'Saldo',
                'verbose_name_plural': 'Saldos',
                'ordering': ['SaldoID'],
            },
        ),
        migrations.CreateModel(
            name='ParticipantesEvento',
            fields=[
                ('ParticipanteID', models.AutoField(primary_key=True, serialize=False)),
                ('Estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10)),
                ('Apodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Eventos_participante', to='api.perfil', to_field='user')),
                ('EventoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.eventos')),
            ],
            options={
                'verbose_name': 'Participante del evento',
                'verbose_name_plural': 'Participantes del evento',
                'ordering': ['ParticipanteID'],
            },
        ),
        migrations.CreateModel(
            name='ParticipantesActividad',
            fields=[
                ('ActividadParticipanteID', models.AutoField(primary_key=True, serialize=False)),
                ('PorcentajeParticipacion', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ValorFijo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ActividadID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.actividades')),
                ('Apodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Actividad_participantes', to='api.perfil', to_field='user')),
            ],
            options={
                'verbose_name': 'Participante de actividad',
                'verbose_name_plural': 'Participantes de actividad',
                'ordering': ['ActividadParticipanteID'],
            },
        ),
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('PagoID', models.AutoField(primary_key=True, serialize=False)),
                ('Valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('FechaPago', models.DateField()),
                ('Completado', models.BooleanField(default=False)),
                ('Acreedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pagos_acreedor', to='api.perfil', to_field='user')),
                ('Deudor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pagos_deudor', to='api.perfil', to_field='user')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'ordering': ['PagoID'],
            },
        ),
        migrations.AddField(
            model_name='eventos',
            name='Creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Eventos_creador', to='api.perfil', to_field='user'),
        ),
        migrations.AddField(
            model_name='actividades',
            name='Creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Actividad_creador', to='api.perfil', to_field='user'),
        ),
        migrations.AddField(
            model_name='actividades',
            name='EventoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.eventos'),
        ),
        migrations.CreateModel(
            name='Contactos',
            fields=[
                ('ContactID', models.AutoField(primary_key=True, serialize=False)),
                ('Estado', models.CharField(choices=[('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada'), ('Pendiente', 'Pendiente'), ('Eliminado', 'Eliminado')], default='Pendiente', max_length=10)),
                ('Emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Contacto_emisor', to='api.perfil', to_field='user')),
                ('Remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Contacto_remitente', to='api.perfil', to_field='user')),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Contactos',
                'ordering': ['ContactID'],
                'unique_together': {('Remitente', 'Emisor'), ('Emisor', 'Remitente')},
            },
        ),
    ]
