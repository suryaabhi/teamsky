var socket = io();

socket.on('connect', function() {
    console.log("CONNECTED");
});

$(document).ready(function() {
    $('#bottomElbow').on('input', function() {
        socket.emit('bottomElbowArticulate', $(this).val());
    });

    $('#topElbow').on('input', function() {
        socket.emit('topElbowArticulate', $(this).val());
    });

    $('#gripper').on('change', function() {
        const isGripped = $(this).is(':checked');
        socket.emit('gripper', isGripped);
    });

    /* Rotate Left */
    document.getElementById('rotateLeft').addEventListener('mousedown', function(event) {
        event.preventDefault();
        console.log('rotate left');
        socket.emit('rotateLeft', {});
    });
    
    document.getElementById('rotateLeft').addEventListener('mouseup', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    document.getElementById('rotateLeft').addEventListener('touchstart', function(event) {
        event.preventDefault();
        console.log('rotate left');
        socket.emit('rotateLeft', {});
    });
    
    document.getElementById('rotateLeft').addEventListener('touchend', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    
    document.getElementById('rotateLeft').addEventListener('touchcancel', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    /* Rotate Left */

    /* Rotate Right */
    document.getElementById('rotateRight').addEventListener('mousedown', function(event) {
        event.preventDefault();
        console.log('rotate right');
        socket.emit('rotateRight', {});
    });
    
    document.getElementById('rotateRight').addEventListener('mouseup', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    document.getElementById('rotateRight').addEventListener('touchstart', function(event) {
        event.preventDefault();
        console.log('rotate right');
        socket.emit('rotateRight', {});
    });
    
    document.getElementById('rotateRight').addEventListener('touchend', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    
    document.getElementById('rotateRight').addEventListener('touchcancel', function(event) {
        event.preventDefault()
        console.log('stop');
        socket.emit('stop', {});
    });
    /* Rotate Right */

    /* Joystick */
    new JoyStick('joyDiv', {}, function(stickData) {
        throttledJoystickHandler(stickData);
    });

    function handleJoystickPositionChange(stickData) {
        console.log("joystick_position_changed");

        socket.emit('joystick_position_changed', {
            data: {x: stickData.x, y: stickData.y}
        });
    }

    const throttledJoystickHandler = throttle(handleJoystickPositionChange, 100);

    function throttle(func, limit) {
        let lastFunc;
        let lastRan;
        return function(...args) {
            const context = this;
            if (!lastRan) {
                func.apply(context, args);
                lastRan = Date.now();
            } else {
                clearTimeout(lastFunc);
                lastFunc = setTimeout(function() {
                    if ((Date.now() - lastRan) >= limit) {
                        func.apply(context, args);
                        lastRan = Date.now();
                    }
                }, limit - (Date.now() - lastRan));
            }
        };
    }
    /* Joystick */
});