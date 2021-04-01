
class GapsDTO:
    def __init__(self, gaps):
        self.name = gaps['name']
        self.gaps = []
        for gap in gaps['gaps']:
            gap_dict = dict()
            gap_dict['id'] = gap['id']
            if 'center' in gap:
                gap_dict['center'] = gap['center']
            if 'action' in gap:
                gap_dict['action'] = gap['action']
            if 'x_init' in gap:
                gap_dict['x_init'] = gap['x_init'] * gaps['scale']
                gap_dict['x_end'] = gap['x_end'] * gaps['scale']

            if 'y_init' in gap:
                gap_dict['y_init'] = gap['y_init'] * gaps['scale']
                gap_dict['y_end'] = gap['y_end'] * gaps['scale']

            self.gaps.append(gap_dict)
