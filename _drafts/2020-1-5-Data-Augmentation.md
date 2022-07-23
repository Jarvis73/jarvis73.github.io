---
layout: post
title: "数据增广 (Data Augmentation)"
date: 2020-01-05 21:19:00 +0800
categories: 图像处理, 机器学习, Python
mathjax: true
# figure: ./images/2020/01/
author: Jarvis
meta: Post
---

* content
{:toc}



## 1. 空间变换 (Spatial Transformation)


## 2. 强度变换 (Intensity Transformation)

### 2.1 [直方图匹配 (Histogram Matching)](https://en.wikipedia.org/wiki/Histogram_matching)

```python
def hist_match(source, template):
    """
    source: np.ndarray
        Image to transform; the histogram is computed over the flattened array
    template: np.ndarray
        Template image; can have different dimensions to source
    
    Returns: np.ndarray
        The transformed output image
    """

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and counts
    _, bin_idx, s_counts = np.unique(source, return_inverse=True, return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    # interp_t_values = np.zeros_like(source,dtype=float)
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)
```
