# 快手爬取个人信息页信息

## 思路
使用手机分享链接，获取分享链接地址，对该地址数据解析

## 字体反爬
因为网页上使用了自定义的字体文件，原来以为只有一套或几套的字体文件，直接做个映射完事。
结果网页上随机返回字体文件，大概100套左右，要是做100个映射，累也累死了。

使用python fonttools工具。解析实时解析字体文件。

![字体](https://github.com/houxiaozhao/kuaishou/blob/master/Snipaste_2020-09-11_15-08-16.png?raw=true)

顺序一直是这个顺序，做了一个讨巧的设置。

```
    uni_list = font.getGlyphOrder()[1:]
    first_map = {}
    for i, uni in enumerate(uni_list):
        if i == 10:
            first_map[uni] = '.'
        elif i == 11:
            first_map[uni] = 'w'
        elif i == 12:
            first_map[uni] = 'k'
        elif i == 13:
            first_map[uni] = 'm'
        elif i == 14:
            first_map[uni] = '+'
        else:
            first_map[uni] = i
    print(first_map)
```

做一个这样的映射关系。

后面就直接替换就可以了。

## 注意获取链接使用手机headers