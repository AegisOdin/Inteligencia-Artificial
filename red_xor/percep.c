#include <assert.h>
#include <math.h>
#include <stdio.h>

static double pesos[2][2] = {{.5,-.4},{-.3,.6}};
static double sesgos[2] = {.1,-.2};
static double salida_pesos[2] = {.7,-.5};
static double salida_sesgo = .1;

static double sigmoide(double z) {
    if (z >= 0) return 1.0 / (1.0 + exp(-z));
    double e = exp(z);
    return e / (1.0 + e);
}

static double predecir(double x, double y, double ocultas[2]) {
    double z = salida_sesgo;
    for (int j = 0; j < 2; ++j) {
        ocultas[j] = sigmoide(pesos[j][0]*x + pesos[j][1]*y + sesgos[j]);
        z += salida_pesos[j]*ocultas[j];
    }
    return sigmoide(z);
}

int main(void) {
    const double datos[4][3] = {{0,0,0},{0,1,1},{1,0,1},{1,1,0}};
    const double tasa = .5;
    assert(sigmoide(0) == .5);
    assert(sigmoide(-1000) == 0 && sigmoide(1000) == 1);
    for (int epoca = 0; epoca < 30000; ++epoca) {
        for (int i = 0; i < 4; ++i) {
            double h[2], x = datos[i][0], y = datos[i][1];
            double resultado = predecir(x,y,h);
            double delta = (datos[i][2]-resultado)*resultado*(1-resultado);
            double delta_oculta[2];
            /* Calcular los gradientes ocultos antes de actualizar los pesos de salida. */
            for (int j = 0; j < 2; ++j)
                delta_oculta[j] = delta*salida_pesos[j]*h[j]*(1-h[j]);
            for (int j = 0; j < 2; ++j) {
                salida_pesos[j] += tasa*delta*h[j];
                pesos[j][0] += tasa*delta_oculta[j]*x;
                pesos[j][1] += tasa*delta_oculta[j]*y;
                sesgos[j] += tasa*delta_oculta[j];
            }
            salida_sesgo += tasa*delta;
        }
    }
    for (int i = 0; i < 4; ++i) {
        double h[2];
        double p = predecir(datos[i][0],datos[i][1],h);
        assert(isfinite(p));
        assert((p >= .5) == (int)datos[i][2]);
        assert(fabs(p-datos[i][2]) < .1);
        printf("%.0f XOR %.0f: %.6f -> %d\n",datos[i][0],datos[i][1],p,p >= .5);
    }
    return 0;
}
