# Copyright (c) 2018 Teledyne LeCroy, all rights reserved worldwide.
#
# This file is part of PySI.
#
# PySI is free software: You can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version
# 3 of the License, or any later version.
#
# This program is distrbuted in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

import math

class Wavelet(object):
	def __init__(self,h):
		self.h=h
		self.L=len(self.h)
		self.g=[pow(-1.,l)*h[self.L-1-l] for l in range(self.L)]
	def DWT(self,xi):
		x=list(xi)
		N=len(x)
		B=self.intlog2(N)-self.intlog2(self.L)+1
		for i in range(B):
			X=list(x)
			for k in range(N/2):
				X[k]=sum([x[(2*k+l)%N]*self.h[l]
					for l in range(self.L)])
				X[k+N/2]=sum([x[(2*k+l+N-2)%N]*self.g[l]
					for l in range(self.L)])
			x=list(X)
			N=N/2
		return X

	def IDWT(self,XI):
		X=list(XI)
		N=len(X)
		B=self.intlog2(N)-self.intlog2(self.L)+1
		N=self.L
		for i in range(B):
			x=list(X)
			for k in range(N/2):
				x[2*k]=sum([self.h[2*l]*X[(k-l+(N/2))%(N/2)]+
						self.g[2*l]*X[(k+1-l+(N/2))%(N/2)+(N/2)]
							for l in range(self.L/2)])
				x[2*k+1]=sum([self.h[2*l+1]*X[(k-l+(N/2))%(N/2)]+
						self.g[2*l+1]*X[(k+1-l+(N/2))%(N/2)+(N/2)]
							for l in range(self.L/2)])
			X=list(x)
			N=2*N
		return x

	@staticmethod
	def intlog2(x):
		r=math.log(float(x))/math.log(2.)
		return int(round(r))

class WaveletDaubechies16(Wavelet):
	def __init__(self):
		Wavelet.__init__(self,[h*math.sqrt(2.)/2
			for h in [0.07695562,0.44246725,0.95548615,0.82781653,
					-0.02238574,-0.40165863,0.000668194,0.18207636,
					-0.0245639,-0.06235021,0.01977216,0.01236884,
					-0.00688771926,-0.000554004549,0.000955229711,-0.000166137261]])

class WaveletDaubechies14(Wavelet):
	def __init__(self):
		Wavelet.__init__(self,[h*math.sqrt(2.)/2
			for h in [0.11009943,0.56079128,1.03114849,0.66437248,-0.20351382,
					-0.31683501,0.1008467,0.11400345,-0.05378245,-0.02343994,
					0.01774979,0.000607514995,-0.00254790472,0.000500226853]])

class WaveletDaubechies8(Wavelet):
	def __init__(self):
		Wavelet.__init__(self,[h*math.sqrt(2.)/2
			for h in [0.32580343,1.01094572,0.8922014,-0.03957503,
					-0.26450717,0.0436163,0.0465036,-0.01498699]])

class WaveletDaubechies4(Wavelet):
	def __init__(self):
		Wavelet.__init__(self,[h*math.sqrt(2.)/2
			for h in [0.6830127,1.1830127,0.3169873,-0.1830127]])

class WaveletHaar(Wavelet):
	def __init__(self):
		Wavelet.__init__(self,[h*math.sqrt(2.)/2
			for h in [1.,1.]])
