from .. import db, bcrypt




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(30), unique=True, nullable=False)
    genero = db.Column(db.String(15), nullable=False)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

    def __init__(self, nombre, apellido, alias, genero, usuario, contraseña):
        self.nombre = nombre
        self.apellido = apellido
        self.alias = alias
        self.genero = genero if isinstance(genero, GenderEnum) else GenderEnum(genero)
        self.usuario = usuario
        self.contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'alias': self.alias,
            'genero': self.genero.value,
            'usuario': self.usuario
        }