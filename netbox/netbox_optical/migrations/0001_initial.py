import django.db.models.deletion
from django.db import migrations, models

import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0001_initial'),
        ('tenancy', '0001_initial'),
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WavelengthGrid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('grid_type', models.CharField(max_length=50)),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'wavelength grid',
                'verbose_name_plural': 'wavelength grids',
            },
        ),
        migrations.CreateModel(
            name='WavelengthChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=50)),
                ('frequency_ghz', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wavelength_nm', models.DecimalField(decimal_places=4, max_digits=10)),
                ('width_ghz', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='netbox_optical.wavelengthgrid')),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['grid', 'frequency_ghz'],
                'verbose_name': 'wavelength channel',
                'verbose_name_plural': 'wavelength channels',
                'unique_together': {('grid', 'name')},
            },
        ),
        migrations.CreateModel(
            name='OpticalCircuit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('status', models.CharField(default='planned', max_length=50)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='optical_circuits', to='netbox_optical.wavelengthchannel')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='optical_circuits', to='tenancy.tenant')),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'optical circuit',
                'verbose_name_plural': 'optical circuits',
            },
        ),
        migrations.CreateModel(
            name='OpticalCircuitHop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('sequence', models.PositiveIntegerField()),
                ('port_role', models.CharField(blank=True, max_length=50)),
                ('optical_circuit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hops', to='netbox_optical.opticalcircuit')),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optical_circuit_hops', to='dcim.interface')),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['optical_circuit', 'sequence'],
                'verbose_name': 'optical circuit hop',
                'verbose_name_plural': 'optical circuit hops',
                'unique_together': {('optical_circuit', 'sequence')},
            },
        ),
        migrations.CreateModel(
            name='MultiplexGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('name', models.CharField(max_length=200)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiplex_groups', to='dcim.device')),
                ('line_interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiplex_line_groups', to='dcim.interface')),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['device', 'name'],
                'verbose_name': 'multiplex group',
                'verbose_name_plural': 'multiplex groups',
                'unique_together': {('device', 'name')},
            },
        ),
        migrations.CreateModel(
            name='MultiplexGroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='netbox_optical.multiplexgroup')),
                ('client_interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiplex_memberships', to='dcim.interface')),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='multiplex_assignments', to='netbox_optical.wavelengthchannel')),
                ('tags', models.ManyToManyField(blank=True, to='extras.tag')),
            ],
            options={
                'ordering': ['group', 'client_interface'],
                'verbose_name': 'multiplex group member',
                'verbose_name_plural': 'multiplex group members',
                'unique_together': {('group', 'client_interface')},
            },
        ),
    ]
