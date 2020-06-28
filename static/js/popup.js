
class PopUp extends HTMLElement {
	constructor() {
		super();
		let root = this.attachShadow({ mode: 'closed' });
		root.appendChild(PopUp.__template.content.cloneNode(true));
		Object.defineProperties(this, {
			__isOpen: {
				enumerable: false,
				writable: true,
				value: false
			},
			__internalNodes: {
				enumerable: false,
				writable: false,
				value: {
					container: root.querySelector('#cntr'),
					content: root.querySelector('#content')
				}
			},
			__eventHandlers: {
				enumerable: false,
				writable: false,
				value: {
					container: (e) => {
						e.stopPropagation();
						if(e.target.isSameNode(this.__internalNodes.container)) {
							this.close();
						}
					},
					content: (e) => {
						e.stopPropagation();
					},
					esckey: ({keyCode}) => {
						if (keyCode == 27) {
							this.close();
						}
					}
				}
			}
		});
    
		root.querySelector('#close_btn').onclick = e => this.close();
		this.__internalNodes.content.addEventListener('click', this.__eventHandlers.content);
		this.__internalNodes.container.addEventListener('click', this.__eventHandlers.container);
	}
	get isOpen() {
		return this.hasAttribute('open');
	}
	set isOpen(value) {
		if(value) {
			this.open();
		} else {
			this.close();
		}
	}
	open(scrollTop = true) {
		if(!this.hasAttribute('open')) {
			this.setAttribute('open', '');
			return;
		}
		if(this.__isOpen) {
			return;
		}
		let allow = true;
		if(typeof this.beforeOpen === "function") {
			allow = this.beforeOpen(this);
		}
		if(allow) {
			document.body.style.overflowY = 'hidden';
			this.style.left = 0;
			window.addEventListener('keyup', this.__eventHandlers.esckey);
			if(scrollTop) {
				this.__internalNodes.content.scrollTop = 0;
			}
			this.__isOpen = true;
			this.dispatchEvent(new CustomEvent('show', {detail: this}));
		} else {
			this.style.left = null;
		}
	}
	close() {
		if(this.hasAttribute('open')) {
			this.removeAttribute('open');
			return;
		}
		if(!this.__isOpen) {
			return;
		}
		let allow = true;
		if(typeof this.beforeClose === 'function') {
			allow = this.beforeClose(this);
		}
		if(allow) {
			document.body.style.overflowY = null;
			this.style.left = null;
			this.__isOpen = false;
			this.dispatchEvent(new CustomEvent('hide', {detail: this}));
		} else {
			this.style.left = 0;
		}
	}

	disconnectedCallback() {
		window.removeEventListener('keyup', this.__eventHandlers.esckey);
	}

	static get observedAttributes() {
		return ['open', 'noeasyclose'];
	}
	attributeChangedCallback(name, oldval, newval) {

		switch(name) {
			case 'open':
				if(newval === null) {
					this.close();
				} else {
					this.open();
				}
				break;
			case 'noeasyclose':
				if(newval === null) {
					this.__internalNodes.content.addEventListener('click', this.__eventHandlers.content);
					this.__internalNodes.container.addEventListener('click', this.__eventHandlers.container);
				} else {
					this.__internalNodes.content.removeEventListener('click', this.__eventHandlers.content);
					this.__internalNodes.container.removeEventListener('click', this.__eventHandlers.container);
				}
				break;
		}
	}
}
Object.defineProperties(PopUp, {
	__template: {
		enumerable: false,
		writable: false,
		value: document.createElement('template')
	},
	tagName: {
		enumerable: true,
		writable: false,
		value: 'pop-up'
	}
});
PopUp.__template.innerHTML =
`<style>
:host {
	--z-index: 1000;
	--border-gap: 1em;
	--content-background: white;
	--content-color: black;
	--content-border: none;
	--content-padding: 0.5em;
	display: flex;
	z-index: var(--z-index);
	background: rgba(0, 0, 0, 0.9);
	color: white;
	position: fixed;
	top: 0;
	left: calc(-1.1 * 100vw);
	box-sizing: border-box;
	overflow: hidden;
	font-size: 1rem;
	transition: left 0.2s;
}
#close_btn {
	z-index: calc(var(--z-index) + 10);
	cursor: pointer;
	position: absolute;
	top: 0.2em;
	right: 0.2em;
	height: 1em;
	width: auto;
	font-size: 1.2em;
	fill: currentColor;
	stroke: #222;
	transition: font-size 0.2s;
}
#close_btn:hover {
	font-size: 1.5em;
}
#cntr {
	display: flex;
	justify-content: center;
	align-items: center;
	cursor: pointer;
	box-sizing: border-box;
	max-width: 100vw;
	width: 100vw;
	max-height: 100vh;
	height: 100vh;
}
:host([noeasyclose]) #cntr {
	cursor: default;
}
#content {
	box-sizing: border-box;
	background: var(--content-background);
	color: var(--content-color);
	border: var(--content-border);
	padding: var(--content-padding);
	cursor: default;
	max-height: calc(100vh - 2 * var(--border-gap));
	max-width: calc(100vw - 2 * var(--border-gap));
	overflow-y: auto;
}
</style>
<div id="cntr">
	<svg id="close_btn" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M23 20.2l-8.2-8.2 8.2-8.2-2.8-2.8-8.2 8.2-8.2-8.2-2.8 2.8 8.2 8.2-8.2 8.2 2.8 2.8 8.2-8.2 8.2 8.2z"/></svg>
<div id="content">
	<slot></slot>
</div>
</div>`;
customElements.define(PopUp.tagName, PopUp);