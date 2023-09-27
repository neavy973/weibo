import sys
import struct


class PeParser:

    def __init__(self, file_path):
        self.MZSIG = b'MZ'
        self.PESIG = b'PE\0\0'
        self.path = file_path

    # 将十六进制数据转换为小端格式的数值
    def get_dword(self, data):
        return struct.unpack('<L', data)[0]

    # 提取ASCII字符串
    def get_string(self, ptr):
        beg = ptr
        while ptr < len(self.data) and self.data[ptr] != 0:
            ptr += 1
        return self.data[beg:ptr]

    def parse(self):
        self.read_data()
        if not self.is_valid_pe():
            print("[Error] Invalid PE file")
        self.parse_import_table()

    # 读取文件数据
    def read_data(self):
        fd = open(self.path, "rb")
        self.data = fd.read()
        fd.close()

    # 检查文件合法性并读取数据
    def is_valid_pe(self):
        temp_ptr = self.get_dword(self.data[0x3c:0x40]) #3C表示是指偏移量,e_lfanew
        if self.PESIG == self.data[temp_ptr:temp_ptr + 4]:
            return True
        else:
            return False

    # RVA转偏移地址
    def rva_to_offset(self, rva):
        h32_size_ptr = self.get_dword(self.data[0x3c:0x40]) + 0x14 #F4
        h32_size = self.get_dword(self.data[h32_size_ptr:h32_size_ptr + 2] + b'\x00\x00') #IMAGE_OPTIONAL_HEADER E0
        temp_rva = self.get_dword(self.data[0x3c:0x40]) + 0x18 + h32_size #1D8
        while True:
            if self.get_dword(self.data[temp_rva + 0xc:temp_rva + 0x10]) + self.get_dword( self.data[temp_rva + 0x10:temp_rva + 0x14]) > rva and self.get_dword( self.data[temp_rva + 0xc:temp_rva + 0x10]) <= rva:
                return rva + self.get_dword(self.data[temp_rva + 20:temp_rva + 24]) - self.get_dword( self.data[temp_rva + 12:temp_rva + 16])
            temp_rva += 40



    # 输入表结构解析
    def parse_import_table(self):
        self.pe_rva = self.get_dword(self.data[0x3c:0x40]) + 0x80
        self.import_table_rva = self.get_dword(self.data[self.pe_rva:self.pe_rva + 4]) #000012D0
        print("%x"%self.import_table_rva)
        self.import_table_size = self.get_dword(self.data[self.pe_rva + 4:self.pe_rva + 8]) #00000078
        print("%x"%self.import_table_size)
        self.import_table_offset = self.get_dword(self.data[self.pe_rva + 8:self.pe_rva + 12]) #00000000
        print("%x"%self.import_table_offset)
        print("rva:\t%d" % self.import_table_rva)
        print("size:\t%d" % self.import_table_size)
        print()

        self.iid_list = []
        ptr_temp = self.rva_to_offset(self.import_table_rva)
        print("%x"%ptr_temp)
        while True:
            iid_list_temp = []
            iid_temp = self.get_dword(self.data[ptr_temp:ptr_temp + 4])
            if iid_temp == 0:
                break
            iid_list_temp.append(iid_temp)
            temp_name=self.get_string(self.rva_to_offset(self.get_dword(self.data[ptr_temp+12:ptr_temp+16])))#获得Name
            iid_list_temp.append(temp_name)
            self.iid_list.append(iid_list_temp)
            ptr_temp += 20
        for i in range(len(self.iid_list)):
            print(str(self.iid_list[i][1], encoding="UTF-8"))
            self.parse_iid_int(self.iid_list[i][0])

    #    解析每个IID对应的IMAGE_THUNK_DATA类型的INT数组
    def parse_iid_int(self, ptr):
        #处理FirstThunk及其之后的函数
        ptr_temp = self.rva_to_offset(ptr)
        while True:
            name_temp = self.get_dword(self.data[ptr_temp:ptr_temp + 4])
            if name_temp == 0:
                break
            print("\t" + str(self.get_string(self.rva_to_offset(name_temp) + 2), encoding="UTF-8"))
            ptr_temp += 4


if __name__ == "__main__":
    if len(sys.argv) == 2:
        p = PeParser(sys.argv[1])
        p.parse()

