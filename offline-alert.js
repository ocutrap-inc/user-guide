import Particle from 'particle:core';

export default function handleDeviceStatus({ event }) {
    if (event.eventName !== 'spark/status') return;
    
    const variablesLedger = Particle.ledger("cloud-only-variables", { deviceId: event.deviceId });
    const { data: variables = {} } = variablesLedger.get();
    
    const now = Date.now();
    const status = event.eventData;
    const OFFLINE_MODE = 5;
    
    console.log(`Received status: ${status} for device: ${event.deviceId}`);
    console.log(`Current hibernation state: ${variables.inHibernation}`);

    // Initialize variables if needed
    if (!variables.lastStatus || !variables.lastStatusTime || variables.inHibernation === undefined) {
        console.log('Initializing status variables');
        variablesLedger.set({
            ...variables,
            lastStatus: status,
            lastStatusTime: now,
            inHibernation: false,
            lastOfflineTime: null
        });
        return;
    }

    // Handle rapid offline->online sequence
    const RAPID_STATUS_CHANGE_THRESHOLD = 1000; // 1 second threshold
    if (status === 'online' && variables.lastStatus === 'offline') {
        const timeSinceLastOffline = now - variables.lastOfflineTime;
        console.log(`Time since last offline: ${timeSinceLastOffline}ms`);
        if (timeSinceLastOffline < RAPID_STATUS_CHANGE_THRESHOLD) {
            console.log('Detected rapid offline->online sequence, suppressing alerts.');
            variablesLedger.set({
                ...variables,
                lastStatus: status,
                lastStatusTime: now
            });
            return;
        }
    }

    // Store offline time and handle offline updates
    if (status === 'offline' && !variables.inHibernation) {
        variables.lastOfflineTime = now;
        console.log('Stored offline time:', now);
        
        // Only publish offline update if not in hibernation
        try {
            const publishSuccess = Particle.publish("offline_update", JSON.stringify({
                power_mode: OFFLINE_MODE,
                timestamp: now
            }), {
                productId: event.productId,
                asDeviceId: event.deviceId
            });
            console.log('Offline update publish result:', publishSuccess);
        } catch (error) {
            console.error('Error publishing offline update:', error);
        }
    }

    // Regular status change handling
    if (status !== variables.lastStatus) {
        console.log(`Status changed from ${variables.lastStatus} to ${status}`);
        console.log(`Hibernation state: ${variables.inHibernation}`);
        
        let alertMessage = null;
        
        if (status === 'online') {
            alertMessage = 'Device back online';
            variables.inHibernation = false;
            console.log('Setting online alert message:', alertMessage);
        } else if (status === 'offline' && !variables.inHibernation) {
            alertMessage = 'Device offline';
            console.log('Setting offline alert message:', alertMessage);
        } else {
            console.log('No alert condition met - status:', status, 'hibernation:', variables.inHibernation);
        }

        if (alertMessage) {
            console.log('Attempting to publish alert:', alertMessage);
            try {
                const publishSuccess = Particle.publish("alert", alertMessage, {
                    productId: event.productId,
                    asDeviceId: event.deviceId
                });
                console.log('Alert publish attempt result:', publishSuccess);
            } catch (error) {
                console.error('Error during alert publish:', error);
            }
        } else {
            console.log('No valid alert message to publish. alertMessage:', alertMessage);
        }
    }

    // Update the stored status
    variablesLedger.set({
        ...variables,
        lastStatus: status,
        lastStatusTime: now
    });
    console.log('Status updated in cloud-only-variables ledger');
}