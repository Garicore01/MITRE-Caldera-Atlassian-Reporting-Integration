## Informe ejecutivo
El informe ejecutivo es un resumen del informe técnico en el cual, un usuario no tecnico 
observar de una manera rapida y sencilla el resultado de la operación y el estado de la/s 
maquinas afectadas
por la operación.

El informe ejecutivo utiliza la información del informe técnico para obtener un

### Partes
- Número de equipos involucrados en la operación
- Estado general de la operación (Crítico-Grave-Moderado-Bajo)
- Porcentaje de exito total
- Porcentaje de exito en cada equipo


### Criterios
En estos criterios no se tienen en cuenta aquellas abilities que esten en la WhiteList. Es 
decir, no se cuentan ni para el porcentaje de exito, ni para el total.

- Si han tenido exito mas del 45% de las abilities, se declara que el estado es Crítico
- Si han tenido exito entre el 25% y 45% de las abilities, se declara que el estado es Grave
- Si han tenido exito entre el 15% y 25% de las abilities, se declara que el estado es Moderado
- Si han tenido exito menos del 15% de las abilities, se declara que el estado es Bajo