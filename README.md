<h1>Show & Tell project</h1>
<hbar>
<p>Got burnt out and cba to do any more</p>

<h2>Example image</h2>
![Example](https://github.com/chromegism/Show-Tell/blob/main/README_Data/image.png)

<h2>Comments</h2>
</br>
<p>Meshes aren't very well implemented as they act both as a data container and as a rendering medium. The camera, which is currently a child of the mesh, should be the parent and also handle the mesh rendering itself. This would make it far easier to do optimisations than it is currently as every mesh needs to have it's data entered into the shader every time as there is no way of telling how the user is going to order the render calls.</p>

