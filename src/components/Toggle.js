import React, { useState } from 'react';

const ToggleButton = () => {
    const [isToggled, setIsToggled] = useState(false);

    const handleToggle = () => {
        setIsToggled(!isToggled);
    };

    return (
        <button onClick={handleToggle}>
            {isToggled ? 'View Similar' : 'Turn On'}
        </button>
    );
};

export default ToggleButton;
