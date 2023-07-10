#  Proyecto Grupal Módulo 7

Cynthia Abarca, Álvaro Manterola, Guido Saavedra, Esteban Santibáñez

Cada entregable de este proyecto será instanciado en una rama con el nombre del aprendizaje correspondiente.

- RFW-004. Permitirá la visualización del historia de pedidos y del detalle de éstos. Desde aquí se le informará al usuario el estado en el que se encuentra su pedido.

    El superuser y staff entrando a la url "pedidos", puede ver todos los pedidos y sus estados, además, pueden ingresar a ver los detalles del pedido, donde pueden cambiar el estado del pedido. Si cambian el estado de un pedido, se envía un mail de notificación al cliente que tenga asignado ese pedido.
    El usuario común puede acceder a la url "pedidos" también, sin embargo solo verá los pedidos que correspondan a su id, teniendo bloqueado el acceso a ver pedidos que no le correspondan. Por medio de una etiqueta puede ver el estado de su pedido. El usuario puede cancelar su pedido sólo si éste se encuentra en los estados pendiente o
en preparación. En caso de estar En despacho, entregado o cancelado, no puede ver el boton para cancelar en el detalle de su pedido.

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
