from rest_framework import serializers

from session.models import User


class UserResponsiveSerializer(serializers.ModelSerializer):
    persona = serializers.CharField(read_only=True, source="persona.get_nombre_completo")
    sessionKey = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    sedes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', "persona", "sessionKey", "sedes", "roles")

    def get_sessionKey(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('sessionKey', None)

    def get_sedes(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('sedes', None)

    def get_roles(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('roles', None)


class UsuarioRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UsuarioSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
