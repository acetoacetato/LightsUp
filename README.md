# IA Para light up

Light up es un puzzle cuyo objetivo es usar ampolletas para iluminar todo el tablero.

## El puzzle

El puzle tiene 2 elementos: Ampolletas y Paredes.
Las ampolletas iluminan en dirección horizontal y vertical hasta que llegan a una pared.
Las paredes pueden contener o no números. En caso de que lo hagan, se debe cumplir la restricción de que debe tener esa cantidad de ampolletas adyacentes a esta (No cuentan diagonales).

## El proyecto

El proyecto consiste en una interfaz gráfica y la IA que resuelve el puzle.
La GUI está hecha en pygame para la visualización y de los pasos que toma la IA para resolverlo.

### Las reglas

Para el desarrollo de la IA se limitó a sólo el uso de reglas, evitando otras técnicas como el backtracking. 

Las reglas propuestas pueden resolver puzles de dificultad fácil y algunos medios en su totalidad:

- Si el número en un cuadrado negro es igual a la cantidad de espacios blancos disponibles adyacentes a este, entonces se inserta una ampolleta en cada uno de estos.
- Si la cantidad de ampolletas adyacentes a una pared es igual al número que tiene dentro de esta, entonces el resto de espacios se llenan con una x, bloqueando la posibilidad de colocar una ampolleta dentro de estos.
- Si una pared contiene un 3, entonces se llenan con una x los 4 espacios diagonales a esta.
- Si un espacio marcado con una x no está iluminado y sólo tiene disponible un espacio (horizontal o vertical) para colocar una ampolleta, en ese espacio se debe colocar una. Cabe destacar que la posición de este espacio puede ser en cualquier distancia, pero no debe estar bloqueado por una pared.
- Si un espacio está vacío, no iluminado y todas los demás espacios en su fila y columna están iluminados, son una pared o están bloqueados, entonces se coloca una ampolleta en este espacio.

## TODO

- [x] Implementar métodos dentro del tablero para insertar ampolletas, bloquear espacios y verificar completitud del puzle.
- [ ] Separar lógica de la interfaz en archivo separado.
- [ ] Crear el loop principal con verificación de reglas para luego aplicarlas.
