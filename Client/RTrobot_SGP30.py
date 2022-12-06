#!/usr/bin/env python3

# SGP30 sensor driver library
# Powered by RTrobot: http://rtrobot.org

import time
import fcntl
import array
import math

I2C_SLAVE=0x0703

class RTrobot_SGP30:
	SGP30_I2CADDR		=	(0x58)

	def __init__(self, i2c_no=1 ,i2c_addr=SGP30_I2CADDR):
		global SGP30_rb , SGP30_wb
		SGP30_rb = open("/dev/i2c-"+str(i2c_no),"rb",buffering=0)
		SGP30_wb = open("/dev/i2c-"+str(i2c_no),"wb",buffering=0)
		fcntl.ioctl(SGP30_rb, I2C_SLAVE, i2c_addr)
		fcntl.ioctl(SGP30_wb, I2C_SLAVE, i2c_addr)
		time.sleep(0.015)


	#SGP30 Initialization
	def SGP30_Init(self):
		SGP30_Serial_ID=RTrobot_SGP30.SGP30_Get_Serial_Id(self)
		if SGP30_Serial_ID==False:
			return False

		if RTrobot_SGP30.SGP30_Get_Feature_Set_Version(self)==False:
			return False

		if RTrobot_SGP30.SGP30_Init_Air_Quality(self)==False:
			return False

		return SGP30_Serial_ID

		
	#SGP30 Get Feature Set Version
	def SGP30_Get_Feature_Set_Version(self):
		buf = [0x20,0x2f]
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,1)


	#SGP30 Get Serial Id
	def SGP30_Get_Serial_Id(self):
		buf = [0x36,0x82]
		SGP30_Serial_ID=RTrobot_SGP30.SGP30_ReadCommand(self,buf,3)
		return SGP30_Serial_ID


	#SGP30 Init Air Quality
	def SGP30_Init_Air_Quality(self):
		buf = [0x20,0x03]
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,0)


	#SGP30 Measure Air Quality
	def SGP30_Measure_Air_Quality(self):
		buf = [0x20,0x08]
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,2)


	#SGP30 Measure Raw Signals
	def SGP30_Measure_Raw_Signals(self):
		buf = [0x20,0x50]
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,2)


	#SGP30 Set Absolute Humidity and Temperature
	def SGP30_Set_Absolute_Humidity(self, temperature , humidity):
		buf=[]
		absolute_humidity=216.7 * (((float)(temperature/100.0) * 6.112 * math.exp((17.62 * temperature) / (243.12 + temperature))) / (273.15 + temperature)) * 1000.0
		if absolute_humidity > 256000:
			return False
		ah_scaled = ((int)(absolute_humidity * 256 * 16777)) >> 24
		buf.append(0x20)
		buf.append(0x61)
		buf.append(ah_scaled >> 8)
		buf.append(ah_scaled & 0xFF)
		tmp=[buf[2],buf[3]]
		buf.append(RTrobot_SGP30.SGP30_Common_Generate_Crc(self,tmp))
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,5)


	#SGP30 Get Iaq Baseline
	def SGP30_Get_Iaq_Baseline(self):
		buf = [0x20,0x15]
		data = RTrobot_SGP30.SGP30_ReadCommand(self,buf,2)
		if data==False:
			return False
		else:
			return (data[0]<<16) | data[1]


	#SGP30 Set Iaq Baseline
	def SGP30_Set_Iaq_Baseline(self,iaq_baseline):
		buf=[]
		buf.append(0x20)
		buf.append(0x1e)
		buf.append(iaq_baseline>>24)
		buf.append(((iaq_baseline & 0x00FF0000)>>16)&0xFF)
		tmp=[buf[2],buf[3]]
		buf.append(RTrobot_SGP30.SGP30_Common_Generate_Crc(self,tmp))
		buf.append(((iaq_baseline & 0x0000FF00)>>8)&0xFF)
		buf.append(iaq_baseline & 0xFF)
		tmp=[buf[5],buf[6]]
		buf.append(RTrobot_SGP30.SGP30_Common_Generate_Crc(self,tmp))
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,0)


	#SGP30 Get Tvoc Baseline
	def SGP30_Get_Tvoc_Baseline(self):
		buf = [0x20,0xb3]
		data = RTrobot_SGP30.SGP30_ReadCommand(self,buf,1)
		if data==False:
			return False
		else:
			return data[0]


	#SGP30 Set Tvoc Baseline
	def SGP30_Set_Tvoc_Baseline(self,tvoc_baseline):
		buf=[]
		buf.append(0x20)
		buf.append(0x77)
		buf.append(tvoc_baseline>>8)
		buf.append(tvoc_baseline&0xFF)
		tmp=[buf[2],buf[3]]
		buf.append(RTrobot_SGP30.SGP30_Common_Generate_Crc(self,tmp))
		return RTrobot_SGP30.SGP30_ReadCommand(self,buf,0)


	#SGP30 Read Command
	def SGP30_ReadCommand(self, buf, read_len):
		pdata=[]
		buf_binary = bytearray(buf)
		SGP30_wb.write(buf_binary)
		time.sleep(0.25)
		tmp = SGP30_rb.read(read_len*3)
		data = array.array('B' , tmp)

		for i in range(read_len*3):
			if (i+1)%3==0:
				#print(i)
				data_crc=[]
				data_crc.append(data[i-2])
				data_crc.append(data[i-1])
				if RTrobot_SGP30.SGP30_Common_Generate_Crc(self, data_crc)!=data[i]:
					return False
				else :
					pdata.append((data[i - 2]<<8)|data[i - 1])
		return pdata


	#SGP30 Common Generate Crc
	def SGP30_Common_Generate_Crc(self, data):
		crc = 0xFF
		for byteCtr in range(2):
			crc ^= data[byteCtr]
			for bit in range(8):
				if crc & 0x80 :
					crc = (crc << 1) ^ 0x131
				else :
					crc = (crc << 1)
		return crc
