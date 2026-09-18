import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PLANO_Y = 0
norte = np.array([0.0,0.0,1.0])
numero_curvas = 300

# mates detras
def proy_estereo(c):
    # c: numero complejo
    a,b = c.real, c.imag
    r2 = a*a + b*b
    denom = 1.0+r2
    return np.array([2*a/denom, 2*b/denom, (r2-1)/denom])

def proy_estereo_array(cs):
    # si usuario elije graficar varios puntos
    a,b=cs.real, cs.imag
    r2 = a*a + b*b
    denom = 1.0+r2
    return np.vstack([2*a/denom, 2*b/denom, (r2-1)/denom])

PLANO_Z = 0
def punto_en_plano(c):
    #grafica el punto en el plano
    return np.array([c.real, c.imag, PLANO_Z])

def descomponer_complejo(s):
    # descompone la cadena de entrada a coomplejo
    s = s.strip().replace(' ','').replace('i','j')
    try:
        return complex(s)
    except:
        raise ValueError(f"La entrada {s} no es valida")
    
# Entrada: Curvas (lineas o circulos)
def entrada_linea(a, b, c, extencion=6.0, n=numero_curvas):
    """Linea a*Re(z)+b*I(z)=c en el plano; regresa un array de lineas (llegan solo |z|<=extencion)"""
    #parametrizacion  
    pts = []
    if abs(b)>abs(a):
        xs = np.linspace(-extencion, extencion, n)
        ys = (c-a*xs)/b
    else:
        ys = np.linspace(-extencion, extencion, n)
        xs = (c-b*ys) /a
    mascara = xs**2+ys**2<=extencion**2
    xs,ys = xs[mascara], ys[mascara]
    return xs+1j*ys

def entrada_circulo(cx,cy,r,n=numero_curvas):
    """circulo centrado en cx+i*cy y radio r"""
    t = np.linspace(0, 2*np.pi, n)
    return (cx+r*np.cos(t))+1j*(cy+r*np.sin(t))


# Dibujo esfera y plano

def dibujar_esfera(ax):
    u = np.linspace(0, 2*np.pi, 80)
    v = np.linspace(0, np.pi, 60)
    X = np.outer(np.cos(u), np.sin(v))
    Y = np.outer(np.sin(u), np.sin(v)) 
    Z = np.outer(np.ones_like(u), np.cos(v)) 
    ax.plot_surface(X, Y, Z, alpha=0.25, color='steelblue', edgecolor='none')

    for z0 in np.linspace(-0.85, 0.85, 7):
        r = np.sqrt(max(0, 1 - z0**2))
        t = np.linspace(0, 2*np.pi, 120)
        ax.plot(r*np.cos(t), r*np.sin(t), np.full_like(t, z0),
                color='steelblue', alpha=0.30, linewidth=0.5)

    for ang in np.linspace(0, np.pi, 9, endpoint=False):
        phi = np.linspace(0, np.pi, 120)
        ax.plot(np.sin(phi)*np.cos(ang), np.sin(phi)*np.sin(ang), np.cos(phi),
                color='steelblue', alpha=0.30, linewidth=0.5)

    t = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), np.zeros_like(t),
            color='steelblue', linewidth=0.9, alpha=0.45)

    ax.scatter(*norte, color='crimson', s=50, zorder=6)
    ax.scatter(0, 0, -1, color='seagreen', s=50, zorder=6)
    ax.text(0, 0, 1.17, '∞ (N)', fontsize=8, color='crimson',  ha='center')
    ax.text(0, 0, -1.25, '0  (S)', fontsize=8, color='seagreen', ha='center')

def dibujar_plano_complejo(ax, extencion=3.0):
    g = np.linspace(-extencion, extencion, 13)
    for xi in g:
        ax.plot([xi, xi], [-extencion, extencion], [PLANO_Z, PLANO_Z],
                color='gray', alpha=0.45, linewidth=0.4)
    for yi in g:
        ax.plot([-extencion, extencion], [yi, yi], [PLANO_Z, PLANO_Z],
                color='gray', alpha=0.45, linewidth=0.4)
    xx, yy = np.meshgrid([-extencion, extencion], [-extencion, extencion])
    zz = np.full_like(xx, PLANO_Z)
    ax.plot_surface(xx, yy, zz, alpha=0.1, color='gold', edgecolor='none')
    ax.plot([-extencion, extencion], [0, 0], [PLANO_Z, PLANO_Z],
            'k-', linewidth=0.8, alpha=0.35)
    ax.plot([0, 0], [-extencion, extencion], [PLANO_Z, PLANO_Z],
            'k-', linewidth=0.8, alpha=0.35)
    ax.text(extencion+0.1, 0, PLANO_Z, 'Re', fontsize=8, color='dimgray')
    ax.text(0, extencion+0.15, PLANO_Z, 'Im', fontsize=8, color='dimgray')

def dibuja_curva(ax, zs, col, label, extencion=3.0, lw=1.6):
    xs = np.clip(zs.real, -extencion*1.5, extencion*1.5)
    ys = np.clip(zs.imag, -extencion*1.5, extencion*1.5)
    ax.plot(xs, ys, np.full_like(xs, PLANO_Z), color=col, linewidth=lw, zorder=5)
    S = proy_estereo_array(zs)
    ax.plot(S[0], S[1], S[2], color=col, linewidth=lw, alpha=0.90, zorder=6, label=label)

def dibuja_punto(ax, c, col, extencion=3.0):
    S = proy_estereo(c)
    P = punto_en_plano(c)
    ax.plot([norte[0], S[0]], [norte[1], S[1]], [norte[2], S[2]],
            color=col, linewidth=1.2, alpha=0.65, linestyle='-')
    ax.plot([S[0], P[0]], [S[1], P[1]], [S[2], P[2]],
            color=col, linewidth=1.0, alpha=0.50, linestyle='--')
    ax.scatter(*S, color=col, s=60, zorder=7)
    ax.scatter(*P, color=col, s=50, zorder=7, marker='D',
               edgecolors='white', linewidths=0.4)
    lbl = formato_complejo(c)
    ax.text(S[0]*1.12, S[1]*1.12, S[2]*1.12, lbl, fontsize=7, color=col)
    ax.text(P[0]+0.05, P[1]+0.05, PLANO_Z,   lbl, fontsize=7, color=col, alpha=0.75)

def formato_complejo(c):
    a, b = c.real, c.imag
    signo = '+' if b >= 0 else '-'
    return f"{a:g}{signo}{abs(b):g}i"
    
# ====== Manejo de entradas =====
def preguntar_objeto():
    print("="*60)
    print(" Proyector estereografico =] (lineas, circulos y puntos)")
    print('='*60)
    print(" Comandos")
    print(" punto 1+2i                  -grafica un solo punto")
    print(" linea   a b c               -grafica linea a*Re + b*Im=c" )
    print(" circulo cx xy r             -grafica un circulo centrado en cx+i*cy de radio r")
    print(" fin / espacio en blanco     -termina y grafica")

    puntos = []
    curvas = []
    colores = plt.cm.tab10(np.linspace(0,0.9,10))
    idx =0

    while True:
        crud = input("  > ").strip()
        if crud.lower() in ('', 'fin'):
            break

        partes = crud.strip().split()
        cmd = partes[0].lower()
        col = colores[idx%10]

        try:
            if cmd == 'punto':
                c = descomponer_complejo(partes[1])
                puntos.append((c,col))
                idx += 1
                print(f'    punto {formato_complejo(c)} anadido')
            
            elif cmd == 'linea':
                a,b,c_val = float(partes[1]), float(partes[2]), float(partes[3])
                zs = entrada_linea(a,b,c_val)
                label = f'linea {a}*Re + {b}*Im = {c_val}'
                curvas.append((label,zs,col))
                idx+=1
                print(f"    {label} anadido")
            
            elif cmd == 'circulo':
                cx, cy, r = float(partes[1]), float(partes[2]), float(partes[3])
                zs    = entrada_circulo(cx, cy, r)
                label = f"circulo |z−({cx}+{cy}i)|={r}"
                curvas.append((label, zs, col))
                idx += 1
                print(f"    {label}  anadido.")
            
            else:
                print("    comando desconcido. Use: punto / linea / circulo / fin")
        except (IndexError, ValueError) as e:
            print(f'    [!]{e}')
    return puntos, curvas

## Graficacion

def graficatodo(puntos, curvas, extencion=3.0):
    fig = plt.figure(figsize=(11,8))
    ax = fig.add_subplot(111, projection='3d')

    dibujar_esfera(ax)
    dibujar_plano_complejo(ax, extencion=extencion)

    for label, zs, col in curvas:
        dibuja_curva(ax, zs, col, label, extencion=extencion)
    for c, col in puntos:
        dibuja_punto(ax, c, col, extencion=extencion)
    
    ax.set_xlabel(' X (Re)',labelpad=3)
    ax.set_ylabel(' Y (Im)',labelpad=3)
    ax.set_zlabel(' Z     ',labelpad=3)
    ax.set_title('Proyeccion esterografica - esfera de Riemann\n curvas en el plano (tenues), circulos en la esfera (brillantes)', fontsize=11)
    ax.set_box_aspect([1,1,1])

    med = (1+PLANO_Z)/2
    prolong = (1-PLANO_Z)/2 +0.4
    ax.set_xlim(-prolong, prolong)
    ax.set_zlim(PLANO_Z-0.2, 1.4)
    ax.set_ylim(-prolong, prolong)
    ax.view_init(elev=18, azim=-55)

    if curvas:
        ax.legend(loc='upper left',fontsize=7,framealpha=0.6)

    plt.tight_layout()
    plt.show()

# entrada de puntos

def main():
    puntos, curvas = preguntar_objeto()

    if not puntos and not curvas:
        print(" Ninguna entrada - mostramos ejemplos =]")
        curvas = [("Circulo unitario |z|=1",  entrada_circulo(0,0,1), plt.cm.tab10(0.0)),
                  ("linea Re(z)=1", entrada_linea(1,0,1),plt.cm.tab10(0.1)),
                  ("linea Im(z)=0 (eje real)", entrada_linea(0,1,0), plt.cm.tab10(0.2))]
        puntos = []
    print(f"\nGraficando {len(puntos)} puntos y {len(curvas)} curvas")
    graficatodo(puntos, curvas)
if __name__ == '__main__':
    main()