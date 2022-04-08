import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Any
import timm
from timm.models import register_model


class MyNet_Metric(nn.Module):
    """
    特征提取网络 输出feature
    """

    def __init__(self, pretrained, model_name, embedding_size):
        super(MyNet_Metric, self).__init__()
        # !!!该属性必须保留，以区分是否为度量学习!!!
        self.embedding_size = embedding_size

        # 特征提取器
        self.features = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=embedding_size,  # 修改输出维度
        )
        self.bn = nn.BatchNorm1d(embedding_size)

    def forward(self, imgs):
        features = self.features(imgs)
        features = self.bn(features)  # 规范化，正则化
        features = F.normalize(features, p=2, dim=1)  # 特征归一化，即模长为1
        return features


"""
注意:
1. @register_model注册为timm模型
2. 命名尽量避免与timm模型重名
"""


@register_model
def mynet_metric(
    pretrained, num_classes, model_name="efficientnet_b0", embedding_size=128
):
    """
    pretrained: 是否加载ImageNet预训练参数（接收timm.create_model传参）
    num_classes: 类别数（接收timm.create_model传参）

    model_name: timm主干网络名
    embedding_size: 特征维度
    """
    print("Backbone_Metric come from user-defined")
    model = MyNet_Metric(pretrained, model_name, embedding_size)
    return model
