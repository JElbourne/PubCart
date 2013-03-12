"""
Created on June 10, 2012
@author: peta15
"""
import logging
from wtforms import fields
from wtforms import Form
from wtforms import validators
from lib import utils
from models import userModels, shoppingModels
from webapp2_extras.i18n import lazy_gettext as _
from webapp2_extras.i18n import ngettext, gettext

FIELD_MAXLENGTH = 50 # intended to stop maliciously long input
FIELD_MAXLENGTH_KEY = 500 # intended to stop maliciously long urlsafe Key input


class FormTranslations(object):
    def gettext(self, string):
        return gettext(string)

    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class BaseForm(Form):
    
    def __init__(self, request_handler):
		super(BaseForm, self).__init__(request_handler.request.POST)
    def _get_translations(self):
        return FormTranslations()

class PreRegisterForm(BaseForm):
	username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Username invalid. Use only letters and numbers.'))])
	email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])

	
class AddAddressForm(BaseForm):
	uk = fields.TextField(_(''), [validators.Required()])
	adn = fields.TextField(_('Address Ref. Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Address Reference Name invalid. Use only letters and numbers.'))])
	ad1 = fields.TextField(_('Address'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	ad2 = fields.TextField(_('Address2'), [validators.Length(max=FIELD_MAXLENGTH)])
	s = fields.TextField(_('State/province'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	c = fields.TextField(_('City'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	z = fields.TextField(_('Zip / Postal Code'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	con = fields.SelectField(_('Country'), choices=utils.COUNTRIES)
    

class ProductSearchForm(BaseForm):
	pn = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	q = fields.IntegerField(_('Quantity'))


class AddProductForm(BaseForm):
	SELLERS = [(None, 'Select a seller...')]
	sellerModels = userModels.Seller.get_all_for_category('electronics')
	for seller in sellerModels:
		SELLERS.append((str(seller.key.urlsafe()),str(seller.n)))
	productNumber = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	urlsafeSellerKey = fields.SelectField(_('Product Seller Number'), choices=SELLERS)
	urlsafeCartKey = fields.HiddenField(_('Cart Number'))


class SimpleChangeQNTForm(BaseForm):
	pk = fields.TextField(_('Product Number'))
	q = fields.IntegerField(_('Quantity'), [validators.Required()])


class ExchangeQNTForm(BaseForm):
	partNumber = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	meq = fields.IntegerField(_('Min Quantity'), [validators.Required()])
	mep = fields.FloatField(_('Min Price'), [validators.Required()])
	percentage = fields.IntegerField(_('Percentage'), [validators.Required()])
	qnt = fields.SelectField(u'Quantity', choices=[('10', '10'),('100', '100'),('250', '250'),('500', '500'), ('1000', '1000'), ('2500', '2500'), ('5000', '5000'), ('10000', '10000')])


class ExchangeOrderForm(BaseForm):
	pn = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	cost = fields.FloatField(_('Cost'), [validators.Required()])
	fee = fields.FloatField(_('Fee'), [validators.Required()])
	bup = fields.FloatField(_('BuyUnitPrice'), [validators.Required()])
	sup = fields.FloatField(_('SellUnitPrice'), [validators.Required()])
	roi = fields.FloatField(_('ROI'), [validators.Required()])
	per = fields.IntegerField(_('Percentage'), [validators.Required()])
	qnt = fields.SelectField(u'Quantity', choices=[('10', '10'),('100', '100'),('250', '250'),('500', '500'), ('1000', '1000'), ('2500', '2500'), ('5000', '5000'), ('10000', '10000')])

class WatchlistForm(BaseForm):
	pk = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	wln = fields.TextField(_('Watchlist Name'), [validators.Length(max=FIELD_MAXLENGTH)])

class WatchlistDeleteForm(BaseForm):
	pk = fields.TextField(_('Product Number'), [validators.Required()])
	wlk = fields.TextField(_('Watchlist Number'), [validators.Required()])
	
class AddToCartForm(BaseForm):
	pk = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	ck = fields.TextField(_('Cart Number'), [validators.Length(max=FIELD_MAXLENGTH_KEY)])
	q = fields.IntegerField(_('QNT'), [validators.Required()])
	lo = fields.TextField(_('Limit Order'), [validators.Length(max=FIELD_MAXLENGTH)])
	lop = fields.FloatField(_('Limit Order Price'))
	cn = fields.TextField(_('Cart Name'), [validators.Length(max=FIELD_MAXLENGTH)])

class DeleteFromCartForm(BaseForm):
	ck = fields.TextField(_('Cart Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	ok = fields.TextField(_('Order Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	ost = fields.IntegerField(_('Order Sub Total'))
	lo = fields.TextField(_('Limit Order'), [validators.Length(max=FIELD_MAXLENGTH)])

class DeleteCartForm(BaseForm):
	ck = fields.TextField(_('Cart Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])

class ChangeQntOfOrderForm(BaseForm):
	ck = fields.TextField(_('Cart Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	ok = fields.TextField(_('Order Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])
	q = fields.IntegerField(_('QNT'), [validators.Required()])

class CreateCartForm(BaseForm):
	CATEGORIES = shoppingModels.Category.getCategoryInfo()
	if not CATEGORIES: CATEGORIES = [('electronics', 'electronics')]
	logging.info('Categories: {}'.format(CATEGORIES))
	name = fields.TextField(_('Cart Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), \
				validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Address Reference Name invalid. Use only letters and numbers.'))])
	description = fields.TextAreaField(_('Description'), [validators.Required()])
	category = fields.SelectField(_('Category'), [validators.AnyOf([cat for cat in CATEGORIES], message=u'A category selection is required')], choices=CATEGORIES)

class ForkCartForm(BaseForm):
	CATEGORIES = shoppingModels.Category.getCategoryInfo()
	if not CATEGORIES: CATEGORIES = [('electronics', 'electronics')]
	logging.info('Categories: {}'.format(CATEGORIES))
	ck = fields.TextField(_('Cart Number'), [validators.Required()])
	name = fields.TextField(_('Cart Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), \
				validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Address Reference Name invalid. Use only letters and numbers.'))])
	description = fields.TextAreaField(_('Description'), [validators.Required()])
	category = fields.SelectField(_('Category'), [validators.AnyOf([cat for cat in CATEGORIES], message=u'A category selection is required')], choices=CATEGORIES)

class CartDetailsForm(BaseForm):
	CATEGORIES = shoppingModels.Category.getCategoryInfo()
	if not CATEGORIES: CATEGORIES = [('electronics', 'electronics')]
	logging.info('Categories: {}'.format(CATEGORIES))
	ck = fields.TextField(_('Cart Number'), [validators.Required()])
	description = fields.TextAreaField(_('Description'), [validators.Required()])
	category = fields.SelectField(_('Category'), [validators.AnyOf([cat for cat in CATEGORIES], message=u'A category selection is required')], choices=CATEGORIES)

class MakeCartDefaultForm(BaseForm):
	ck = fields.TextField(_('Cart Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_KEY)])

class CopyOrderForm(BaseForm):
	ock = fields.TextField(_('Original Cart Number'), [validators.Required()])
	nck = fields.TextField(_('New Cart Number'), [validators.Required()])

class CreateAlertForm(BaseForm):
	pk = fields.TextField(_('Product Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	aq = fields.IntegerField(_('Alert Quantity'), [validators.Optional()])
	ap = fields.FloatField(_('Alert Price'), [validators.Optional()])

class PaypalPaymentForm(BaseForm):
	ck = fields.TextField(_('Cart Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	ogt = fields.IntegerField(_('Order Grand Total'), [validators.Required()])

class EditSellerForm(BaseForm):
	CATEGORIES = shoppingModels.Category.getCategoryInfo()
	if not CATEGORIES: CATEGORIES = [('electronics', 'electronics')]
	logging.info('Categories: {}'.format(CATEGORIES))
	n = fields.TextField(_('Seller Company Number'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	dom = fields.TextField(_('Domain'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	cn = fields.TextField(_('Contact Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
	pn = fields.IntegerField(_('Phone Number'), [validators.Required()])
	cat = fields.SelectField(_('Category'), [validators.AnyOf([cat for cat in CATEGORIES], message=u'A category selection is required')], choices=CATEGORIES)

