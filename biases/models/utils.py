import torch
import torch.nn as nn
from lie_conv.lieConv import Swish
import math


def FCtanh(chin, chout, zero_bias=False, orthogonal_init=False):
    return nn.Sequential(Linear(chin, chout, zero_bias, orthogonal_init), nn.Tanh())


def FCswish(chin, chout, zero_bias=False, orthogonal_init=False):
    return nn.Sequential(Linear(chin, chout, zero_bias, orthogonal_init), Swish())


def FCsoftplus(chin, chout, zero_bias=False, orthogonal_init=False):
    return nn.Sequential(Linear(chin, chout, zero_bias, orthogonal_init), nn.Softplus())


def Linear(chin, chout, zero_bias=False, orthogonal_init=False):
    linear = nn.Linear(chin, chout)
    if zero_bias:
        torch.nn.init.zeros_(linear.bias)
    if orthogonal_init:
        torch.nn.init.orthogonal_(linear.weight)
    return linear


class Reshape(nn.Module):
    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        return x.view(self.shape)


def tril_mask(square_mat):
    n = square_mat.size(-1)
    coords = torch.arange(n)
    return coords <= coords.view(n, 1)


def mod_angles(q, angular_dims):
    assert q.ndim == 2
    D = q.size(-1)
    non_angular_dims = list(set(range(D)) - set(angular_dims))
    q_modded_dims = (q[..., angular_dims] + math.pi) % (2 * math.pi) - math.pi
    q_non_modded_dims = q[..., non_angular_dims]
    return torch.cat([q_modded_dims, q_non_modded_dims], dim=-1)