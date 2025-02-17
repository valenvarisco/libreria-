# -*- coding: utf-8 -*-
"""Libreria

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yUsUhhUFq2WkUnOLfMRCsidopAZibU5M
"""

class ResumenNumerico:
  pass


class ResumenGrafico:
  pass


class GeneradoraDeDatos:
  pass
class Regresion:
  def __init__(self, x,y):
        self.x = x
        self.y = y

  def coef_correlacion(self):
    print('Coeficiencite de correlacion:', np.corrcoef(self.x,self.y)[0,1])

  def estimaciones(self):
    betas = self.resultado.params()
    valores_ajustados = self.resultado.fittedvalues
    p_valores = self.resultado.pvalues
    errores = self.resultado.bse
    lista = {"parametros": betas, "bse": errores,"p-valores":p_valores,"valores_ajustados":valores_ajustados}
    print('Los coeficientes son:',betas,'Los valores ajustados son:',valores_ajustados)
    print('Los errores estandars de cada coef son:',errores,'Los p-valores son:',p_valores)
    return lista

  def supuestos(self):
    residuos = self.resultado.resid()
    residuos_z = (residuos-np.mean(residuos))/np.std(residuos)
    plt.scatter(self.valores_ajustados,residuos)
    sm.qqplot(residuos_z,line='45')
    return residuos

  def prediccion(self,x_new):
    predicciones = self.resultado.predict(x_new)
    return predicciones

  def grafica(self):
    plt.scatter(self.x, self.y, marker="o", facecolors="none", edgecolors="blue")
    plt.plot(self.x,self.valores_ajustados)
    plt.xlabel("Predictora")
    plt.ylabel("Respuesta");


class RegresionLineal(Regresion):
  def __init__(self, x, y):
        super().__init__(x, y)

  def modelo(self):
    X = sm.add_constant(self.x)
    modelo = sm.OLS(self.y, X)
    self.resultado = modelo.fit()

  def intervalos(self,x_new,alfa):
    prediccion = self.resultado.get_prediction(x_new)
    int_pred = prediccion.conf_int(obs=True,alpha=alfa)
    int_conf =prediccion.conf_int(alpha=alfa)
    lista = {"Intervalo de pred": int_pred, "Intervalo de confi": int_conf}
    return lista

  def r_cuadrado(self):
    r_cuadrado = self.resultado.rsquared
    r_ajustado = self.resultado.rsquared_adj
    return r_cuadrado, r_ajustado

  pass


class RegresionLogistica(Regresion):
  def __init__(self, x, y):
        super().__init__(x, y)

  def modelo(self):
    X = sm.add_constant(self.x)
    modelo = sm.Logit(self.y, X)
    self.resultado = modelo.fit()

  def matriz_conf(self,x_train,y_train,x_test,y_test,umbral):
    self.y_test = y_test
    self.x_test = x_test
    X = sm.add_constant(x_train)
    modelo_train = sm.Logit(y_train,X)
    resultado_tr = modelo_train.fit()
    X_test = sm.add_constant(x_test)
    self.probabilidades = resultado_tr.predict(X_test)
    self.y_pred = 1*(self.probabilidades>=umbral)
    a = sum((self.y_pred==1) & (y_test==1))
    b = sum((self.y_pred==1) & (y_test==0))
    c = sum((self.y_pred==0) & (y_test==1))
    d = sum((self.y_pred==0) & (y_test==0))
    error = (b + c)/len(self.y_test)
    print('El error de mala clasificación es:', error)
    lista = {"Verdaderos positivos": a, "Falsos positivos": b,"Verdaderos negativos":d,"Falsos negativos":c}
    return lista

  def sens_esp(self):
    grilla = np.linspace(0,1,100)
    sensi = []
    espe = []
    for i in grilla:
      y_pred1= 1*(self.probabilidades>=i)
      np.array(sensi.append(sum((y_pred1==1) & (self.y_test==1))/sum(self.y_test)))
      np.array(espe.append(sum((y_pred1==0) & (self.y_test==0))/(len(self.x_test)-sum(self.y_test))))

    promedios = sensi+(espe-1)
    punto_corte = float(grilla[np.where(max(promedios)==promedios)])
    sensibilidad = float(sensi[np.where(max(promedios)==promedios)])
    especificidad = float(espe[np.where(max(promedios)==promedios)])
    lista = {"punto de corte": punto_corte, "sensibilidad": sensibilidad,"especificidad":especificidad}
    plt.plot(1-np.array(espe),sensi);
    plt.xlabel('1-especificidad')
    plt.ylabel('sensibilidad')
    return lista



  pass