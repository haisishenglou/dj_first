from rest_framework import serializers
from .models import BookInfo


#  使用默认提供的序列话器
class BookInfoserializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型对象
        model = BookInfo
        #  __all__展示所有字段
        fields = "__all__"
        #  read_only_fields指明只读字段，即仅用于序列化输出的字段
        read_only_fields = ('id', 'bread', 'bcomment')
        #  extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
        extra_kwargs = {
            'bread': {'min_value': 0, 'required': True},
            'bcomment': {'min_value': 0, 'required': True},
        }


# 重写 to_representations方法
class BookRelatedField(serializers.RelatedField):
    """自定义用于处理图书的字段"""
    def to_representation(self, value):
        return "Book: %d, %s" % (value.id, value.btitle)


# 自定义book序列化器
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="id", required=True)
    btitle = serializers.CharField(label="书名", max_length=20, required=True)
    bpub_date = serializers.DateField(label="出版时间", required=False)
    bread = serializers.IntegerField(label="阅读量", required=False)
    bcomment = serializers.IntegerField(label="评论量", required=False)
    image = serializers.ImageField(label="图片", required=False)

    #  自定义验证，验证btitle字段
    def validata_btitle(self, value):

        if "django" not in value.lower():
            raise serializers.ValidationError("图书不是关于Django")
        return value

    #  自定义验证，验证bread<bcomment,验证多字段
    def validate(self, attrs):
        bread = attrs['bread']
        bcomment = attrs['bcomment']
        if bread < bcomment:
            raise serializers.ValidationError('阅读量小于评论量')
        return attrs

    def create(self, validated_data):
        """新建"""
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance

# 自定义hero序列化器
class HeroSerializer(serializers.Serializer):
    GENDER_CHOICES = ((0, 'made'), (1, "femade"))
    id = serializers.IntegerField(label="id", required=True)
    hname = serializers.CharField(label="姓名", max_length=6, required=True)
    hgender = serializers.ChoiceField(label="性别", choices=GENDER_CHOICES, default=0, required=False)
    hcomment = serializers.CharField(label="介绍", max_length=200, allow_null=True, required=False)
    # 查询hero对应书名
    # hbook = serializers.StringRelatedField(label="图书")
    #  通过hero查询对应书籍信息
    # hbook = BookInfoserializer()

    #  展示自定义图书字段
    hbook = BookRelatedField(read_only=True)
