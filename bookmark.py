# -*- coding: utf-8 -*-
'''
Bookmarks entities.

@author: Mariano Ruiz
'''


from osv import osv
from osv import fields
from tools.translate import _
import logging

logger = logging.getLogger('bookmark')
logger.setLevel(logging.WARN)

class bookmark_tag(osv.osv):
    '''Tag Entity Model'''
    _name = 'bookmark.tag'
    _description = "Bookmark Tag"
    _columns = {
            'name': fields.char('Name', size=64, required=True,
                        readonly=False, states={'disapproved': [('readonly', True)]}),
            'state': fields.selection([
                        ("new", "New"),
                        ("approved", "Approved"),
                        ("disapproved", "Disapproved")],
                        "State", readonly=True)
        }
    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'The name of the tag must be unique.')
        ]

    def create(self, cr, uid, vals, context=None):
        tag_id = super(bookmark_tag, self).create(cr, uid, vals, context=context)
        if self.currentuser_is_bookmark_manager(cr, uid):
            self.tag_approved(cr, uid, [tag_id])
        self.log(cr, uid, tag_id, _('Bookmark Tag "%s" is created.') % vals['name'])
        return tag_id

    def tag_new(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'new' })
        return True

    def tag_approved(self, cr, uid, ids):
        if self.currentuser_is_bookmark_manager(cr, uid):
            self.write(cr, uid, ids, { 'state' : 'approved' })
            return True
        raise osv.except_osv(_('Error'), _('You cannot perform the operation. "Bookmark / Manager" users only.'))

    def tag_disapproved(self, cr, uid, ids):
        if self.currentuser_is_bookmark_manager(cr, uid):
            self.write(cr, uid, ids, { 'state' : 'disapproved' })
            return True
        raise osv.except_osv(_('Error'), _('You cannot perform the operation. "Bookmark / Manager" users only.'))

    def currentuser_is_bookmark_manager(self, cr, uid):
        user_rec = self.pool.get('res.users').browse(cr, uid, uid)
        user_groups = user_rec['groups_id']
        bookmark_manager_group_id = self.pool.get('res.groups').search(cr, uid, [('name', '=', 'Bookmark / Manager')])[0]
        for group_rec in user_groups:
            if group_rec.id == bookmark_manager_group_id:
                return True
        return False
        

bookmark_tag()


class bookmark(osv.osv):
    '''Bookmark Entity Model'''
    _name = 'bookmark.bookmark'
    _description = "Bookmark"
    _columns = {
            'name': fields.char('Name', size=200, required=True),
            'description': fields.text('Description'),
            'url': fields.char('URL', size=1000, required=True),
            'tag_ids': fields.many2many('bookmark.tag', 'bookmark_tags_rel',
                'bookmark_id', 'tag_id', 'Bookmark tags'),
        }
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the bookmark must be unique.'),
        ('url_uniq', 'unique (url)', 'The URL of the bookmark must be unique.')
    ]

    def create(self, cr, uid, vals, context=None):
        tag_recs = self.pool.get('bookmark.tag').browse(cr, uid, vals['tag_ids'][0][2])
        for tag_rec in tag_recs:
            self.__check_tag_state(tag_rec)
        book_id = super(bookmark, self).create(cr, uid, vals, context=context)
        self.log(cr, uid, book_id, _('Bookmark "%s" is created.') % vals['name'])
        return book_id

    def write(self, cr, uid, ids, vals, context=None):
        if 'tag_ids' in vals:
            tag_recs = self.pool.get('bookmark.tag').browse(cr, uid, vals['tag_ids'][0][2])
            for tag_rec in tag_recs:
                self.__check_tag_state(tag_rec)
        return super(bookmark, self).write(cr, uid, ids, vals, context=context)

    def __check_tag_state(self, tag_rec):
        if tag_rec['state'] == 'approved':
            logger.debug("Tag state validation OK")
            return
        elif tag_rec['state'] == 'disapproved':
            raise osv.except_osv(_('Error'), _('The tag "%s" chosen was disapproved.') % tag_rec['name'])
        elif tag_rec['state'] == 'new':
            raise osv.except_osv(_('Error'), _('The tag "%s" chosen was not approved yet.') % tag_rec['name'])
        else:
            logger.error('Unknown state "%s" from tag "%s"' % (tag_rec['state'], tag_rec['name']))
            raise osv.except_osv(_('Error'), _('Unknown tag state.'))

bookmark()

class bookmark_tag2(osv.osv):
    _inherit = 'bookmark.tag'
    _columns = {
            'bookmark_ids': fields.many2many('bookmark.bookmark', 'bookmark_tags_rel',
                'tag_id', 'bookmark_id', 'Bookmarks'),
    }

bookmark_tag2()
