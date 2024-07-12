from rest_framework import serializers

from api.models import Camion, Ruta, RutaDetalle


class CamionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camion
        fields = '__all__'

    def validate(self, attrs):
        if self.instance:
            if Camion.objects.filter(placa=attrs['placa']).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({'detail': 'Ya existe un camión con esa placa'})
        else:
            if Camion.objects.filter(placa=attrs['placa']).exists():
                raise serializers.ValidationError({'detail': 'Ya existe un camión con esa placa'})

        if self.instance:
            if Camion.objects.filter(chofer=attrs['chofer']).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({'detail': 'El chofer ya está asignado a otro camión'})
        else:
            if Camion.objects.filter(chofer=attrs['chofer']).exists():
                raise serializers.ValidationError({'detail': 'El chofer ya está asignado a otro camión'})
        return attrs


class RutaSerializer(serializers.ModelSerializer):
    camion = CamionSerializer(
        read_only=True,
    )
    camion_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Camion.objects.all(),
        source='camion'
    )

    class Meta:
        model = Ruta
        fields = '__all__'

    def validate(self, attrs):
        if self.instance is None:
            if not attrs['camion'].estado:
                raise serializers.ValidationError({'detail': 'El camión no está disponible'})
        return attrs


class RutaDetalleSerializer(serializers.ModelSerializer):
    ruta_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Ruta.objects.all(),
        source='ruta'
    )
    entregado = serializers.BooleanField(
        read_only=True,
        default=False
    )

    class Meta:
        model = RutaDetalle
        fields = ['surtidor', 'orden', 'litros', 'ruta_id', 'entregado']


class RutaWithDetalleSerializer(serializers.ModelSerializer):
    detalle = RutaDetalleSerializer(
        many=True, read_only=True,
        source='ruta_detalle_ruta'
    )
    camion = CamionSerializer(
        read_only=True
    )

    class Meta:
        model = Ruta
        fields = ['id', 'nombre', 'fecha', 'estado',
                  'litros', 'tipo_gasolina', 'precio_litro',
                  'camion', 'detalle',
        ]
