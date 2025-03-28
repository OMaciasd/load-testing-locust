import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

# Datos de las pruebas
estres = [2000, 1900, 1800, 1700, 1600, 1500, 1400, 1300]
carga = [997, 960, 915, 832, 682, 566, 412, 280]
fallas = [93.2, 58, 56, 50, 43, 40, 38, 18]
latencia = [13000, 46000, 188000, 50000, 60000, 70000, 80000, 30000]
rps = [93.2, 0.1, 0.1, 0.4, 0.2, 0.4, 0.4, 0.3]

# Normalización de RPS
rps_min, rps_max = min(rps), max(rps)
rps_norm = [(val - rps_min) / (rps_max - rps_min) * 100 if rps_max != rps_min else 50 for val in rps]

# Configuración del gráfico
fig, ax1 = plt.subplots(figsize=(9, 5))

# Eje izquierdo: Usuarios en simultáneo y Fallas
ax1.set_xlabel("Tiempo de Estrés (segundos)", fontsize=10)
ax1.set_ylabel("Usuarios en simultáneo / Fallas (%)", fontsize=10, color="tab:blue")
ax1.plot(estres, carga, marker="o", linestyle="-", color="tab:blue", label="Usuarios en simultáneo", zorder=3)
ax1.plot(estres, fallas, marker="s", linestyle="--", color="tab:red", label="Fallas (%)", zorder=3)
ax1.tick_params(axis="y", labelcolor="tab:blue", labelsize=9)

# Eje derecho: Latencia
ax2 = ax1.twinx()
ax2.set_ylabel("Latencia (ms) (p95 - SLO)", fontsize=10, color="brown")
ax2.set_yscale("linear")  # Escala lineal
ax2.set_ylim(0, max(latencia) * 1.1)  # Ajusta según necesidad

ax2.plot(estres, latencia, marker="^", linestyle="-", color="darkorange", label="Latencia",
         zorder=9, linewidth=0.8, alpha=1.0)
ax2.tick_params(axis="y", labelcolor="brown", labelsize=9)

# Eje adicional para RPS
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))  # Separar más el eje derecho
ax3.set_ylabel("RPS (normalizado) (Tasa de Peticiones por Segundo)", fontsize=10, color="tab:purple")
ax3.plot(estres, rps_norm, marker="d", linestyle=":", color="tab:purple", label="RPS (ajustado)",
         zorder=2, linewidth=2, alpha=0.7)
ax3.tick_params(axis="y", labelcolor="tab:purple", labelsize=9)

# Líneas horizontales con anotaciones
ax1.axhline(y=300, color="red", linestyle="--", linewidth=2, alpha=0.5, zorder=1)
ax1.axhline(y=400, color="green", linestyle="--", linewidth=2, alpha=0.5, zorder=1)

# Coordenada X central para las etiquetas
x_center = np.mean(estres)

ax1.text(x_center, 320, "Ratio 0.2 - Falsos positivos", color="red", zorder=10, fontsize=9, fontweight="bold",
         verticalalignment="bottom", horizontalalignment="center",
         bbox=dict(facecolor="white", alpha=0.9, edgecolor="black", boxstyle="round,pad=0.3"))

ax1.text(x_center, 420, "Ratio 0.3 - Común en aplicaciones móviles", color="green", zorder=10, fontsize=9, fontweight="bold",
         verticalalignment="bottom", horizontalalignment="center",
         bbox=dict(facecolor="white", alpha=0.9, edgecolor="black", boxstyle="round,pad=0.3"))

# Ajuste de leyendas
legend1 = ax1.legend(loc="upper left", fontsize=9)
legend = ax2.legend(loc="upper center", fontsize=11, framealpha=1, edgecolor="black",
                    prop={'weight': 'bold', 'size': 12, 'family': 'sans-serif'},
                    facecolor="white", fancybox=True, labelcolor='black')

legend3 = ax3.legend(loc="lower center", fontsize=9)

for text in legend.get_texts():
    text.set_path_effects([path_effects.Stroke(linewidth=0.8, foreground='gray'),
                           path_effects.Normal()])


# Aplicar efecto a la leyenda de RPS
for text in legend3.get_texts():
    text.set_path_effects([path_effects.Stroke(linewidth=0.8, foreground='gray'),
                           path_effects.Normal()])

plt.title("Comparación de Consumo de Recursos", fontsize=11, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.5)

plt.show()
