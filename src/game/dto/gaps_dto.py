
class GapsDTO:
    def __init__(self, gaps):
        self.name = gaps['name']
        self.h_gaps = []
        for gap in gaps['h_gaps']:
            gap_dict = dict()
            if 'action' in gap:
                gap_dict['action'] = gap['action']
            gap_dict['init'] = gap['init'] * gaps['scale']
            gap_dict['end'] = gap['end'] * gaps['scale']
            self.h_gaps.append(gap_dict)

        self.v_gaps = []
        for gap in gaps['v_gaps']:
            gap_dict = dict()
            if 'action' in gap:
                gap_dict['action'] = gap['action']
            gap_dict['init'] = gap['init'] * gaps['scale']
            gap_dict['end'] = gap['end'] * gaps['scale']
            self.v_gaps.append(gap_dict)
