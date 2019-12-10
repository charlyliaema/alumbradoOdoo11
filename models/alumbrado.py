# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

from odoo.addons.base_geoengine import geo_model
from odoo.addons.base_geoengine import fields as geo_fields
#import psycopg2
#from odoo.addons.base_geoengine.fields import GeoPoint
#from osgeo import ogr


class luminarias(geo_model.GeoModel):
	_name = 'alumbrado.luminarias'
	_rec_name = 'xap_comp'

	xap_comp = fields.Char(string="Código compuesto")
	xap = fields.Integer(string="Código de la luminaría")
	cvecol = fields.Many2one('alumbrado.colonias',string="Clave de la colonia")
	cvecalle = fields.Char(string="Codigo de la calle")
	calle = fields.Char(string="Calle")
	tipo_c = fields.Char(string="tipo de calle")
	entre = fields.Char(string="entre que calles")
	t_piso = fields.Char(string="tipo de piso")
	nivel_c = fields.Char(string="nivel de la calle")
	ancho_c = fields.Char(string="ancho de la calle")
	mod_lam = fields.Char(string="modelo de la lampara")
	tecno = fields.Char(string="tecnologia led, vs, fluoresente")
	capac_pot = fields.Char(string="capacidad de potencia watts")
	marca_foco = fields.Char(string="marca de foco")
	marca_bala = fields.Char(string="marca de balastra")
	
	perdidas = fields.Integer(string="datod e perdidas de energia")
	
	tension = fields.Char(string="tension baja o alta")
	
	tipodeilum = fields.Char(string="tipo de iluminacion")
	
	zona_cfe = fields.Char(string="zona de cfe")
	tipoposte = fields.Char(string="tipo de poste")
	no_lum = fields.Float(string="numero de luminarios en el poste")
	altura_p = fields.Float(string="altura del poste")
	altura_lum = fields.Char(string="altura del luminario")
	brazo = fields.Char(string="numero de brazos en el poste")
	
	jefe_cua = fields.Char(string="jefe de cuadrilla")
	unidad = fields.Integer(string="numero de vehiculo")
	
	fecha_cens = fields.Date(string="fecha del censo")
	imagen = fields.Char(string="imagen de los luminarios")
	x = fields.Float(string="Coordenada X")
	y = fields.Float(string="Coordenada Y")
	observ = fields.Char(string="observaciones del poste, poda o limunario")
	servicio = fields.Char(string="tipo de servicio de cfe medido o estimado")
	rpu = fields.Char(string="numero de rpu cfe")
	medidor = fields.Char(string="numero de medidor cfe")
	geom = geo_fields.GeoPoint(string='Punto', srid=4326)

	def genera_cod_comp(self):
		self.xap_comp = self.cvecol + self.xap

	def ConvertGeoJson(self, gjson, from_srid=4326, to_srid=3857):
		"""
		H.Stivalet 2019-09-25
		Convierte el tipo de proyección en formato GeoJson usando funciones de PostGis. Requiere que la Base de datos de Odoo tenga instalada la estención de PosyGis
		params:
			gjson(str): GeoJson de un Point, Line o Polygon
			from_srid(int): SRID de entrada
			to_srid(int): SRID de salida
		returns: (str) GeoJson con la nueva proyección del Point, Line o Polygon
		"""
		if not isinstance(gjson, str) or gjson == '':
			return ''
		query = "select ST_AsGeoJSON(st_transform(st_setsrid(st_geomfromgeojson('" + gjson + "')," + str(from_srid) + ")," + str(to_srid) + "))"
		self._cr.execute(query)
		data = self._cr.fetchone()
		if data:
			gjson = data[0]
		return gjson

	@api.model#necesita hacer algo en el nivel del modelo en sí, no solo algunos registros. #api.model para estructuras de modelos, métodos auxiliares, etc.
	def create(self, values):
		if 'geom' in values and values['geom'] != '':
			values['geom'] = self.ConvertGeoJson(values['geom'], 3857, 4326)
		return super(luminarias, self).create(values)

	@api.multi#api.multi se usa para funciones en las que desea realizar alguna operación en uno o varios registros. Un ejemplo aquí puede ser establecer un campo en múltiples registros:
	def write(self, values):
		if 'geom' in values and values['aggeomeb_polygon'] != '':
			values['geom'] = self.ConvertGeoJson(values['geom'], 3857, 4326)
		return super(luminarias, self).write(values)

	@api.multi
	def read(self, fields=None, load='_classic_read'):
		record = super(luminarias, self).read(fields, load=load)
		if len(record) == 1 and 'geom' in record[0] and record[0]['ageb_polygon'] != '':
			record[0]['geom'] = self.ConvertGeoJson(record[0]['geom'])
		return record


class colonias(models.Model):
	_name = 'alumbrado.colonias'

	name = fields.Char(string="Colonia")


class reportes(models.Model):
	_name = 'alumbrado.reportes'

	name = fields.Selection([('A','Apagado'),('E','Encendido'),('I','Intermitente'),('B','Luz Baja')], string="Motivo de peticion")
	description = fields.Text(string='Descripcion detallada')
	solicitante = fields.Many2one(comodel_name='res.partner', string="Solicitante")
	luminaria = fields.Many2one(comodel_name='alumbrado.luminarias', string="Luminaria")#hereda todo el modelo luminarias?#######
	colonia = fields.Many2one(comodel_name='alumbrado.colonias', string="Colonia", related="luminaria.cvecol") #store=True#########related
	estatus = fields.Selection([('N','Nuevo'),('P','En proceso'),('A','Atendido')], string="Estatus")
	

class vehiculo(models.Model):
	_name = 'alumbrado.vehiculo'

	numero = fields.Char(string="numero del vehiculo")
	tipoVehiculo = fields.Selection([('C','Camioneta'),('G','Grua Normal'),('A','Corto Alcance')], string="Tipo de vehiculo")
	marca = fields.Char(string="Marca del Vehiculo")
	modelo = fields.Date(string="Modelo del vehiculo")
	placas = fields.Char(string="numero de placas")


class jefe_cuadrilla(models.Model):
	_name = 'alumbrado.jefe_cuadrilla'

	cuadrilla = fields.Many2one(comodel_name='res.partner', string="Jefe de Cuadrilla")
	numero = fields.Many2one(comodel_name='alumbrado.vehiculo', string="numero de vehiculo")
	telefono = fields.Char(string="telefono del Jefe de cuadrilla", related="cuadrilla.phone")
	turno = fields.Selection([('M','Matutino'),('V','Vespertino'),('F','Fin de Semana'),('S','Sabado')], string="Turno de jefe de Cuadrilla")


#####################################################################################################################
class atencion_reportes(models.Model):
	_name = 'alumbrado.atencion_reportes'

	#id = fields.Many2one(comodel_name='alumbrado.reportes', string="numero de reporte")#como poner el id
	numero = fields.Many2one(comodel_name='alumbrado.vehiculo', string="numero de vehiculo")
	turno = fields.Many2one(comodel_name='alumbrado.jefe_cuadrilla', string="Turno de jefe de Cuadrilla")
	cuadrilla = fields.Many2one(comodel_name='res.partner', string="Jefe de Cuadrilla")


class respuestas_atencion(models.Model):
	_name = 'alumbrado.respuestas_atencion'

	estatus = fields.Many2one(comodel_name='alumbrado.reportes', string="Estatus")
	material = fields.Many2one(comodel_name='alumbrado.almacen', string="material del almacen")
	motivo = fields.Selection([('B','Falta Balastra'),('C','Falta Cable'),('F','Falta Grua'),('G','Falta Escalera Grande'),('F','Falta Foco'),('M','Falta Material'),('P','Falta Poste')], string="Motivo No se atendio")


class almacen(models.Model):
	_name = 'alumbrado.almacen'

	material = fields.Char(string="material del almacen")
	vale = fields.Char(string="numero de vale")
	factura = fields.Char(string="numero de factura")
	proveedor = fields.Char(string="Preveedor")#¿provedor se pone en res.partner?
	recibe = fields.Char(string="nombre de quien recibe material")#¿recibe se pone en res.partner?
########################################################################################################################