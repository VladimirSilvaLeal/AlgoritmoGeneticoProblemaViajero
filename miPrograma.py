import matplotlib.pyplot as plt
import random
from scipy import stats
import numpy as np

coordenadas=[(20,20),(20,40),(20,160),(40,120),(60,20),(60,80),(60,200),(80,180),(100,40),(100,120),(100,160),(120,80),(140,140),(140,180),(160,20),(180,60),(180,100),(180,200),(200,40),(200,160)]

rta=[(180,60),(200,40),(160,20),(100,40),(60,20),(20,20),(20,40),(60,80),(40,120),(20,160),(60,200),(80,180),(100,160),(100,120),(140,180),(180,200),(200,160),(180,100),(140,140),(120,80)]

def graficar_plano(puntos):
    x_val = [x[0] for x in puntos]
    y_val = [x[1] for x in puntos]
    x_val.append(puntos[0][0])
    y_val.append(puntos[0][1])
    plt.figure(2)
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.grid()
    plt.show()

# Ejecuta en Orden 3° (Dentro del Orden 2°)
# Funcion objetivo o fitness (Calculo de lista de sumatorias)
def aptitud(puntos): # El parametro de entrada llamado "puntos" realmente es un cromosoma, es decir un individuo, una ruta cualqueira, o una posible solucion, 
    L=len(puntos) # Se calcula la LONGITUD de elementos del cromosoma, es decir 20.
    r=0.0 # La variable r, realmente es la distancia calculada, que llamaremos TRAMO CALCULADO.
    for i in range(0,L-2): # pregunta --> ¿Porque el rango va de 0 a 18? ------> Es numero 18 porque se empieza a contar en cero, y la ultima se suma abajito, fuera del for.
        x=abs(puntos[i][0]-puntos[i+1][0]) # ---> Dentro del for se calcula la distancia entre coordenadas con la formula con ese mismo nombre.
        y=abs(puntos[i][1]-puntos[i+1][1])
        r=r+pow((x**2+y**2),1/2)
    x=abs(puntos[0][0]-puntos[-1][0]) # Se repite el calculo de la distancia, pero desde la posicion 0, hasta la ultima, es decir [-1]
    y=abs(puntos[0][1]-puntos[-1][1])
    r=r+pow((x**2+y**2),1/2)    
    return r # Retorna la distacia total sumada del cromosoma #1

# Ejecuta en Orden 1° ---> itera 20 veces el for.
# Itera 20 veces creando listas aleatorias.
def poblacion(cant_ind):
    pop=[] # Almacena la Matriz -------------------> Como cada elemento agregado es una lista, una lista de listas se convierte en una matriz.
    for i in range(cant_ind): # Itera 20 Veces ------------> Porque la cantidad de "ciudades" es 20 como variable global ---> cantidad_individuos=20
        random.shuffle(coordenadas) # Los Mezcla -------------------> Genera una mezcla los elementos de la lista reorganizandolos aleatoriamente
        pop.append(coordenadas.copy()) # Copia la mezcla y la agrega ---------> Hace una copia de la mezcla anterior, y la agrega a la lista pop, como lo que agrega como elementos es una LISTA, pop se convierte en una matriz.
    return pop # Retorna la Matriz 20 x 20 Aleatorizada

# Ejecuta en Orden 2°
# Recorre la matriz aleatorizada "pop" ---> guarda la sumatoria calculada en f o sea la LISTA DE SUMATORIAS, una
def evaluar(pop):
    f=[] # ------> Guarda una lista de sumatorias de distancias..  
    for i in pop: # La variable iteradora i trae todo el cromosoma de la posicion cero, de la matriz aleatorizada 20 x 20
        f.append(aptitud(i)) # Retorna la sumatoria de la distancia calculada del cromosoma iterado
    return f

def  rel_freq (x): 
    freqs = [x.count(value) / len (x) for value in set (x)] 
    return freqs
# Ejecuta en Orden 4°
def seleccion(apt,pop,k): # apt = Lista_de_Sumatorias, pop = Poblacion inicial (Matriz20x20), k = cantidad de individuos es decir 20 
    fi=(1-(stats.zscore(np.array(apt))))+3   # np.array(apt) nos disponibiliza los valores conviertiendo la lsita de sumatorias en una matriz de 1 fila por 20 columnas, con elementos accesibles.   //    zscore calcula a cuantas desviaciones estandar se aleja el punto, respecto a la media.
    prob=fi/sum(fi) # Se le asigna la porcion de la ruleta proporcional a cada sumatoria de la lista.
    new_pop=[] #Valor que se retorna despues de girar la ruleta
    for i in range (k):
        puntero=0 #Es el que me permite apuntar hacia el cromosoma seleccionado
        acumulador=0 #Probabilidad acumulada
        mem=[] # Se utiliza como memoria
        while(acumulador<random.random()): #Se opera la ruleta, analogo a girarv la ruleta
            mem=pop[puntero] # El puntero apunta al primer cromosoma, en la posicion cero del la matriz
            acumulador=acumulador+prob[puntero]
            puntero+=1 
        new_pop.append(mem)
    return new_pop

def rotate(seq, k):
    return seq[k:] + seq[:k]

def Animar(mapa):
    for i in mapa:
        x_val = [x[0] for x in i]
        y_val = [x[1] for x in i]
        x_val.append(i[0][0])
        y_val.append(i[0][1])
        plt.cla()
        plt.plot(x_val,y_val)
        plt.plot(x_val,y_val,'or')
        plt.grid()
        plt.pause(0.5)
        plt.draw()
        plt.show()


        
if __name__=="__main__": # Aqui se inicializa el programa
    cantidad_individuos=20 # Es lo mismo que cant de puntos, ciudades, o cantidad de cromosomas en una pobacion.
    Generaciones=10000 # Se refiere a la cantidad de iteraciones en el tiempo, para obtener la mejor solucion SOBREVIVIENTE.
    Ejecuciones=10 # 
    Mejor_todos=[]
    Peor_todos=[]
    Promedio_Todos=[]
    Mejor_mapa=[]
    mejor_f1a=10000 # Mejor fila se debiese llamar mejor ruta, mejor cromosoma, o mas generalizado solucion  optima
    mejor_f1b=0
    for j in range(Ejecuciones):
        mejor=[]
        peor=[]
        promedio=[]
        Mejores_mapas_ani=[]
        #Población inicial
        P0=poblacion(cantidad_individuos) # Retorna la Matriz 20 x 20 aleatorizada.
        f=evaluar(P0) # Recibe como parametro la Matrix Aleatorizada y retorna la LISTA_DE_SUMATORIAS
        # Aqui f debe ser renombrado como lista_de_sumatorias
        a1=np.argmin(f) # numpy.argmin retorna el indice donde esta ubicado el valor mas pequeño, en este caso, la ruta mas corta ---> y luego de tener el indice vuelve y se ejecuta la funcion aptitud, para tener CUANTA DISTANCIA FUE LA MINIMA
        b1=np.argmin(f) 
        ind_mem_a1=P0[a1] # Guarda las coordenadas de la mejor ruta o mejor cromosoma
        ind_mem_b1=P0[b1] # Repite lo mismo que ahorita pero lo guarda en otra variable
        fa1=aptitud(ind_mem_a1) # como ya tenemos la ruta, aqui vuelve y calcula la distacia, para guardarla en la variable fa1
        fb1=aptitud(ind_mem_b1) # Repite lo mismo guardando el mismo valor pero ahora en la variable fb1
        for i in range(Generaciones):
            #Seleccion
            P1=seleccion(f,P0,cantidad_individuos) # Como parametro envia ----> f que es la lista aleatorizada, P0 que es la poblacion inicial (matriz 20 x 20)  y cantidad de individuos, es decir 20 y retorna un vector con 20 candidatos
            f1=evaluar(P1)   #Calcula la distancia de cada uno de los 20 individuos y los almacena en f1

            #Mutación
            sel_ind=random.randint(0,cantidad_individuos-1)  #Se selecciona aleatoriamente un individuo
            ind_sel=P1[sel_ind].copy() #Asigna a la vatiable ind_sel las ubicaciones del individuo seleccionado
            a=random.randint(0,len(ind_sel)-1) # Ee toma la posición de una ubicacion aleatoria del individuo   
            b=random.randint(0,len(ind_sel)-1) # Se toma otra posición aleatoria del mismo individuo para realizar el intercambio y crear un nuevo individuo
            aux=ind_sel[a] # selecciona las coordenadas ubicadas en la posición a del individuo seleccionado
            ind_sel[a]=ind_sel[b] # Se asigna a la posición (a), las coordenadas que s e encuentran ubicadas en la posicion (b) 
            ind_sel[b]=aux  # Se asigna a la posición (b), las coordenadas que s e encuentran ubicadas en la posicion (a)
            P1[sel_ind]=ind_sel.copy()  # P1 reemplaza en la matriz (poblacion) el nuevo individuo mutado 
            
            #Cruce
            sel_ind=random.randint(0,cantidad_individuos-1) #Se selecciona aleatoriamente un individuo dentro de la población seleccionada en la ruleta
            sel_coor=random.randint(1,len(ind_mem_a1)-1) # Selecciona el umbral de la posición del individuo que se cruzara
            r11=P1[sel_ind].copy() # asigna las coordenadas del individuo seleccionado en r11, es un metodo para crear una copia de una lista existente en este caso selecciona el individuo de una poblacion.
            r12=r11[0:sel_coor].copy()  # Asigna a r12 el valor de la posición cero hasta el umbral aleatorio del individuo seleccionado 
            r13=r11[sel_coor:len(r11)].copy() # se asigna a r13 los valores de las coordenas restantes del individuo desde el umnbral aleatorio
            if(random.random()<0.5):  # Se hace un aleatorio entre cero y uno, si es menor que (0,5), entonces cruza los varores de la primera parte que es r12, si no, rota la segunda parte que es r13
                random.shuffle(r12)
            else:
                random.shuffle(r13)
            r14=r12+r13 # En esta paso se construye el nuevo individuo
            P1[sel_ind]=r14.copy()  # reemplaza el individuo cruzado en la matriz de población.
            
            #Reemplazo generacional por estado estable
            f1=evaluar(P1) # Vuelve y se calculan todas las distancias de la nueva poblacion con los cambios geneticos y se suman (ruta total)
            b1=np.argmin(f1) # Calcula el indice (ubica el indice menor valor) de la menor distancia de los individuos de la poblacion. 
            ind_mem_b1=P1[b1] # Selecciona la mejor ruta dentro de la población
            fb1=aptitud(ind_mem_b1) # Calcula la menor distancia para la ruta total.
            Mejores_mapas_ani.append(ind_mem_b1)
            if(fb1<fa1): # Si la nueva menor distancia calculada de la nueva poblacion es menor a la poblacion es menor a la distancia es menor a la distancia a la mejor distancia de la poblacion anterior
                fa1=fb1
                ind_mem_a1=ind_mem_b1
                Mejores_mapas_ani.append(ind_mem_a1) 
                
            if(fa1<=min(f1)): # Si no se cumple lo anterior, entonces asigna los valores de la generacion anterior a la poblacion actual
                gg=ind_mem_a1.copy()
                for i in range(0,int(cantidad_individuos)):
                    sel_ind=i
                    if(i==0):
                        k=0
                    else:
                        k=random.randint(1,len(ind_mem_a1)-1)
                    gg = rotate(ind_mem_a1, k)
                    P0[sel_ind]=gg.copy()
            #Almacenar para la grafica
            f1=evaluar(P0)
            mejor.append(min(f1))
            peor.append(max(f1))
            promedio.append(sum(f1)/len(f1))
            #Publicar mapa
            mejor_f1b=aptitud(ind_mem_a1)
        if(mejor_f1b<mejor_f1a):
            mejor_f1a=mejor_f1b
            Mejor_mapa=ind_mem_a1
        #Resultados finales
        Mejor_todos.append(min(mejor))
        Peor_todos.append(max(mejor))
        Promedio_Todos.append(sum(mejor)/len(mejor))
        
    #plt.ion()
    #Animar(Mejores_mapas_ani)
    #Datos ultima ejecución
    plt.figure(0)
    plt.plot(mejor)
    plt.plot(peor)
    plt.plot(promedio)
    plt.grid()
    #Datos evaluaciones
    plt.figure(1)
    plt.plot(Mejor_todos)
    plt.plot(Peor_todos)
    plt.plot(Promedio_Todos)
    plt.grid()
    plt.show()
    graficar_plano(Mejor_mapa)
    print(aptitud(Mejor_mapa))
    print(aptitud(rta))