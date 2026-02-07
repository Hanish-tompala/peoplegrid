(() => {
    // 1. PRESERVE THE ORIGINAL FUNCTION
    // We keep a copy of the real preventDefault just in case we need it for non-copy stuff.
    const nativePreventDefault = Event.prototype.preventDefault;

    // 2. OVERRIDE THE BLOCKING MECHANISM
    // We redefine what preventDefault does for the entire page.
    Event.prototype.preventDefault = function() {
        // Check if the event is something we want to force-enable
        const isClipboardEvent = ['copy', 'cut', 'paste', 'contextmenu'].includes(this.type);
        
        // Check if it's a keyboard shortcut for copy/paste (Ctrl+C, Ctrl+V, etc.)
        const isKeyBlock = this.type === 'keydown' && (
            (this.ctrlKey || this.metaKey) && 
            ['c', 'v', 'x', 'a', 'C', 'V', 'X', 'A'].includes(this.key)
        );

        if (isClipboardEvent || isKeyBlock) {
            // THE BYPASS:
            // We do absolutely nothing here. 
            // The site thinks it blocked the action, but the browser ignores them.
            // console.log("Bypassed site restriction on:", this.type);
            return; 
        }

        // For all other events (like clicking a button), let the site function normally.
        return nativePreventDefault.apply(this, arguments);
    };

    // 3. STOP PROPAGATION BLOCKING
    // Some sites try to stop the event from bubbling up. We disable that tool for them too.
    const nativeStopProp = Event.prototype.stopPropagation;
    Event.prototype.stopPropagation = function() {
        const isClipboardEvent = ['copy', 'cut', 'paste', 'contextmenu'].includes(this.type);
        if (isClipboardEvent) return;
        return nativeStopProp.apply(this, arguments);
    };

    // 4. NUKE INLINE HANDLERS (The Cleanup Crew)
    // This clears things like <input onpaste="return false">
    const nuke = () => {
        const events = ['oncopy', 'oncut', 'onpaste', 'oncontextmenu', 'onselectstart', 'ondragstart'];
        const targets = [window, document, document.body];
        
        // Scan common targets
        targets.forEach(t => {
            if(!t) return;
            events.forEach(evt => {
                if (t[evt]) t[evt] = null;
            });
        });

        // Scan all input and textarea fields specifically
        document.querySelectorAll('input, textarea').forEach(el => {
             events.forEach(evt => {
                if (el[evt]) el[evt] = null;
            });
        });
    };

    // Run nuke immediately and every 2 seconds to catch dynamic content
    nuke();
    setInterval(nuke, 2000);

})();