import random
import statistics
import simpy
#Funcion para la ejecucion de procesos
def proceso(numProceso, env, cpu, ram, waiting, tiempoLlegada):
    global tiempoTotal #guarda el tiempo total de los procesos
    global tiempoProcesos #Lista que guarda cuanto le toma a cada proceso
    yield env.timeout(tiempoLlegada)
    start = env.now
    end = 0
    print ('Llegada del proceso %d en el momento %s ' % (numProceso, start))
    instrucciones = random.randint(1,10) #Cuantas instrucciones tiene el proceso
    ramProceso = random.randint(1,10) #Cuanta ram necesita el proceso
    with ram.get(ramProceso) as cola:
        print ('El proceso # %d entra a la RAM en %s' % (numProceso, env.now))
        print ('El espacio que necesita el proceso %d en la RAM: %s' % (numProceso, ramProceso))
        while instrucciones > 0:
            with cpu.request() as cola1: #Cpu con sus colas
                yield cola1
                print ('El proceso %d entra al CPU en %s' % (numProceso, env.now))
                yield env.timeout(1)
                instrucciones = instrucciones - 3 #Ejecuta solo 3 instrucciones
                if instrucciones <= 0: #Interrumpe el proceso porque ya termino
                    instructions = 0
                    end = env.now 
                    print ('El proceso %d sale del CPU en el momento %s' %(numProceso, end)) 
                else: #Mira si pasa a waiting o a ready
                    opcion = random.randint(1,2)
                    if (opcion == 1):
                        with waiting.request() as cola2:
                            yield cola2
                            yield env.timeout(1)
    tiempo = end - start #tiempo de ejecucion
    tiempoProcesos.append(tiempo) 
    tiempoTotal = end

#Variables necesarias para la simulacion                        
env = simpy.Environment()
ram = simpy.Container(env, capacity = 100)
cpu = simpy.Resource(env, capacity = 1)
waiting = simpy.Resource(env, capacity = 1)
random.seed(555)
intervalo = 10.0
tiempoTotal = 0
tiempoProcesos = []
totalInstrucciones = 25

#Estos son los procesos en el enviroment ejecutara
for i in range (totalInstrucciones):
    env.process(proceso(i, env, cpu, ram, waiting, random.expovariate(1.0/intervalo)))

#correr el programa
env.run()

#calculo de promedio y desviacion estandar
promedio = tiempoTotal/totalInstrucciones
desviacion = statistics.stdev(tiempoProcesos)


print ('Tiempo total', tiempoTotal)
print('Promedio de tiempo por instruccion: ', promedio)
print('Desviacion Estandar: ', desviacion)