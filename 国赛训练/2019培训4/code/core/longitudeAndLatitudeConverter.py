from core.const import (
    LONGITUDE_LOWER,
    LATITUDE_LOWER
)


def lalConverter(position: list) -> slice:
    '''
    # longitude and latitude converter
    - args
        - position:list
    - return
        - slice
    > 坐标从经纬度各自数值最小点开始计算为0，此公式仅适用于北纬23°附近,**纬度优先**
    '''
    return (
        (position[0] - LATITUDE_LOWER) * 111,
        (position[1] - LONGITUDE_LOWER) * 102.1760
    )
