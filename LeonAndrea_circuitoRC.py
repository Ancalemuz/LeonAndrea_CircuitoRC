import numpy as np
import matplotlib.pyplot as plt

datos=np.genfromtxt("CircuitoRC.txt")
tiempo=datos[:,0]
q=datos[:,1]
v=10.0

cg=np.random.random()*20
rg=np.random.random()*20

def paso(c,r):
	o=np.random.normal(c,0.1)
	p=np.random.normal(r,0.1)
	return o,p

def calcularq(c,r):
	qfinal=[]
	qfinal=v*c*(1-np.exp(-tiempo/(r*c)))
	return qfinal

def mc(cguess,rguess):
	clista=[]
	rlista=[]
	l=[]
	qmc=[]
	chi=[]
	n=0
	lactual=0.0
	qmc=v*cguess*(1-np.exp(-tiempo/(rguess*cguess)))
	chi=((q-qmc)**2)
	chicuadrado=(sum(chi))/10000
	exponente=np.exp(-0.5*chicuadrado)
	l.append(exponente)
	clista.append(cguess)
	rlista.append(rguess)
	for j in range(1,10000):
		c1,r1=paso(cguess,rguess)
		qmc=v*c1*(1-np.exp(-tiempo/(r1*c1)))
		chi=((q-qmc)**2)
		chicuadrado=(sum(chi)/10000)
		lactual=np.exp(-0.5*chicuadrado)
		a=lactual/l[j-1]
		if(a>1):
			clista.append(c1)
			rlista.append(r1)
			l.insert(j,lactual)
			cguess=c1
			rguess=r1
			c1,r1=paso(c1,r1)
		else:
			b=np.random.random()
			if(a>b):
				clista.append(c1)
				rlista.append(r1)
				l.insert(j,lactual)	
				cguess=c1
				rguess=r1
				c1,r1=paso(c1,r1)	
			else:
				clista.append(cguess)
				rlista.append(rguess)
				l.insert(j,l[j-1])
	return clista,rlista,l

listafinalc,listafinalr,listal=mc(cg,rg)
posicion=np.argmax(listal)
qoptimo=calcularq(listafinalc[posicion],listafinalr[posicion])

print("mejor C:",listafinalc[posicion], "Mejor R:",listafinalr[posicion],"Qmax es:", v*listafinalc[posicion])
plt.figure()
plt.title("tiempo vs q")
plt.plot(tiempo,q)
plt.plot(tiempo,qoptimo)
plt.savefig("CargaRC.pdf")


plt.figure()
plt.title("C vs L")
plt.scatter(listafinalc,-np.log(listal))
plt.yscale('log')
plt.savefig("C.pdf")

plt.figure()
plt.title("R vs L")
plt.scatter(listafinalr,-np.log(listal))
plt.yscale('log')
plt.savefig("R.pdf")


