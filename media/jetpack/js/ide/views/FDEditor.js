/*
 * File: jetpack/FDEditor.js
 * Provides functionality for the Jetpack/Capability Editor
 *
 * Class which provides basic wrapper.
 * Its functionalities should be overwritten in specific classes (Bespin.js, etc.)
 * Otherwise standard textarea will be used.
 */
var Class = require('shipyard/class/Class'),
	Events = require('shipyard/class/Events'),
	Options = require('shipyard/class/Options'),
	object = require('shipyard/utils/object');

// globals: Element, Spinner, fd

var FDEditor = module.exports = new Class({

	Implements: [Options, Events],

    options: {
        element_type: 'textarea'
    },

	$name: 'FlightDeckEditor',

    items: {},

    current: false,

	initialize: function(wrapper, options) {
		this.setOptions(options);
        // create empty editor
        this.element = new Element(this.options.element_type,{
            'text': '',
            'class': 'UI_Editor_Area'
        });
        this.element.inject(wrapper);
		this.spinner = new Spinner('editor-wrapper');
		this.changed = false;
        // prepare change events
        this.boundWhenItemChanged = this.whenItemChanged.bind(this);
        this.boundSetContent = this.setContent.bind(this);
        this.addEvent('setContent', function(c) {
            this.switching = false;
        });
    },

    registerItem: function(uid, item){
        this.items[uid] = item; 
    },

    getItem: function(uid){
        return this.items[uid];
    },

    deactivateCurrent: function(){
        // deactivate and store changes                   
        this.current.active = false;
        // store changes
        this.dumpCurrent();
    },

    activateItem: function(item){
        // activate load and hook events
        var editor = this;
        this.current = item;
        this.current.active = true;
        if (!this.current.isLoaded()) {
            this.spinner.show();
			this.setContent('', true);
            this.current.loadContent(function(content) {
                if (item == editor.current) {
                    editor.setContent(content);
                    editor.spinner.hide();
                }
                //else another file has become active
            });
        } else {
            this.setContent(this.current.get('content'));
			this.spinner.hide();
        }
        if (this.current.get('readonly')) {
            this.setReadOnly();
        } else {
            this.setEditable();
        }
        this.setSyntax(this.current.get('ext'));
    },

    switchTo: function(uid){
        $log('FD: DEBUG: FDEditor.switchTo ' + uid);
        var self = this;
        this.switching = true;
        var item = this.getItem(uid);
        if (!item) {
            //this.registerItem(item);
            $log('no item wtf');
        }
        if (this.current) {
            this.deactivateCurrent();
        }
        this.activateItem(item);
        return this;
    },

    dumpCurrent: function() {
        this.current.set('content', this.getContent());
        return this;
    },

    setReadOnly: function() {
        this.element.set('readonly', 'readonly');
        if (this.change_hooked) {
            this.unhookChange();
        }
    },

    setEditable: function() {
        if (this.element.get('readonly')) { 
            this.element.erase('readonly');
        }
        this.hookChangeIfNeeded();
    },
    
    cleanChangeState: function(){
        object.forEach(this.items, function(item){
            item.setChanged(false);
            item.change_hooked = false;
            // refresh original content
            item.original_content = item.get('content');
        });
        this.hookChangeIfNeeded();
    },

    hookChangeIfNeeded: function() {
        if (!this.current.get('readonly')) {
            if (!this.current.changed && !this.change_hooked) {
                this.hookChange();
            } else if (this.current.changed && this.change_hooked) {
                this.unhookChange();
            }
        }
    },

    hookChange: function(){
        this.element.addEvent('keyup', this.boundWhenItemChanged);
        this.change_hooked = true;
	},

    unhookChange: function(){
        this.element.removeEvent('keyup', this.boundWhenItemChanged);
        this.change_hooked = false;
        $log('FD: INFO: No longer following changes');
    },

    whenItemChanged: function() {
        if (!this.switching && this.getContent() != this.current.original_content) {
            this.current.setChanged(true);
            this.fireEvent('change');
            $log('DEBUG: changed, code is considered dirty and will remain'+
                    'be treated as such even if changes are reverted');
            this.unhookChange();
        } else if (!this.switching && this.current.changed) {
            this.current.setChanged(false);
        }
    },

	getContent: function() {
		return this.element.value;
	},

	setContent: function(value, quiet) {
        this._setContent(value);
        if (!quiet) this.fireEvent('setContent', value);
		return this;
	},
	
	_setContent: function(value) {
		this.element.set('value', value);
	},

    isChanged: function() {
        return this.items.some(function(item) {
            return item.changed;
        });
    },

    setSyntax: function(){},
	
	focus: function() {
		this.editor.focus();
		this.fireEvent('focus');
	},
	
	blur: function() {
		this.editor.blur();
		this.fireEvent('blur');
	}
});
