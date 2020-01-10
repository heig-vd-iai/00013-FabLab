import ezdxf
from os import path, mkdir

class File():
    def __init__(self, path):
        assert(isinstance(path,str))
        self.path = path

    def toDXF(self, foldername = 'DXFs'):
        name = self.path.replace('\\','/').split('/')
        name[-1] = name[-1].replace('png', 'dxf')
        name[-2] = foldername

        folder = '/'.join(name[:-1])
        if not path.isdir(folder):
            mkdir(folder)

        return DXF_File('/'.join(name))


class DXF_File(File):
    def __init__(self,path):
        super().__init__(path)

    def fillDXF(self, pts):
        doc = ezdxf.new(dxfversion = 'R2010')
        msp = doc.modelspace()

        for k in range(0,len(pts)):
            p = (pts[k,0], pts[k,1])
            q = (pts[k-1,0], pts[k-1,1])

            msp.add_line(p,q)

        doc.saveas(self.path)
