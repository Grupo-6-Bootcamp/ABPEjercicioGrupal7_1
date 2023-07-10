#  Proyecto Grupal Módulo 7

Cynthia Abarca, Álvaro Manterola, Guido Saavedra, Esteban Santibáñez

Cada entregable de este proyecto será instanciado en una rama con el nombre del aprendizaje correspondiente.

En esta última etapa se agregaron las imágenes a los productos, de tal forma que los usuarios que tomen pedidos puedan ver lo que están agregando. Por conveniencia y para no sobrecargar la base de datos, las imágenes son almacenadas en una carpeta local /media/ y referenciadas desde los templates correspondientes.

En la página principal es posible navegar por los productos disponibles, revisando sus detalles (imagen, descripción, stock y precio). Cualquier visitante a la página puede ver el listado de productos y el detalle de estos, pero las funciones para crear una Wishlist están restringidas para clientes registrados.

Una vez registrados, los clientes podrán seleccionar los productos que quieran y agregarlos a una wishlist. Posteriormente pueden o no continuar con la compra, pasando a la etapa de Pedidos en donde se definirán la dirección de entrega y la forma de pago. Este pedido se identifica con un número único.


# Usuarios

Para configurar un nuevo usuario utilizamos la siguiente extension:

https://chrome.google.com/webstore/detail/temp-mail-disposable-temp/inojafojbhdpnehkhhfjalgjjobnhomj
 

De esta forma pudimos verificar inmediatamente si los correos se enviaban correctamente, además de ser necesario tener un correo para
poder recibir la contraseña generada de forma automatica al registrarse.

De igual forma, al registrarse un usuario, sus datos de registro (username, email y contraseña) se imprimen en la terminal que ejecuta el proyecto

Para el login se configuró el email en lugar del username.

<table>
    <thead>
          <th>Email</th>
          <th>Contraseña</th>
          <th>Clase</th>
    </thead>
    <tbody>
          <tr>
            <td>admin@admin.cl</td>
            <td>123</td>
            <td>Superuser</td>
          </tr>
          <tr>
            <td>staff@staff.cl</td>
            <td>C5sjzJEK</td>
            <td>Staff</td>
          </tr>
          <tr>
            <td>dawobag952@meogl.com</td>
            <td>ramaZaP9</td>
            <td>Usuario Comun</td>
          </tr>
    </tbody>
</table>
