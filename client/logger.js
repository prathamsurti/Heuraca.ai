/**
 * Simple logging utility for Figma plugin
 */
const Logger = (function() {
  // Log levels
  const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
    NONE: 4
  };

  // Default configuration
  let config = {
    level: LOG_LEVELS.INFO,
    enabled: true,
    logToConsole: true,
    logToUI: false,
    logElement: null
  };

  // Format the current time for logs
  function getTimestamp() {
    const now = new Date();
    return now.toISOString().replace('T', ' ').substr(0, 19);
  }

  // Format a log message
  function formatMessage(level, context, message, data) {
    let formattedMessage = `[${getTimestamp()}] [${level}]`;
    
    if (context) {
      formattedMessage += ` [${context}]`;
    }
    
    formattedMessage += `: ${message}`;
    
    if (data !== undefined) {
      if (typeof data === 'object') {
        try {
          formattedMessage += ` - ${JSON.stringify(data)}`;
        } catch (e) {
          formattedMessage += ' - [Object cannot be stringified]';
        }
      } else {
        formattedMessage += ` - ${data}`;
      }
    }
    
    return formattedMessage;
  }

  // Log to console
  function logToConsole(level, message) {
    if (!config.logToConsole) return;
    
    switch(level) {
      case 'DEBUG':
        console.debug(message);
        break;
      case 'INFO':
        console.info(message);
        break;
      case 'WARN':
        console.warn(message);
        break;
      case 'ERROR':
        console.error(message);
        break;
      default:
        console.log(message);
    }
  }

  // Log to UI if enabled
  function logToUI(message) {
    if (!config.logToUI || !config.logElement) return;
    
    try {
      const element = document.getElementById(config.logElement);
      if (element) {
        const logLine = document.createElement('div');
        logLine.textContent = message;
        element.appendChild(logLine);
        
        // Auto-scroll to bottom
        element.scrollTop = element.scrollHeight;
      }
    } catch (e) {
      console.error('Failed to log to UI:', e);
    }
  }

  // Main log function
  function log(level, context, message, data) {
    if (!config.enabled || LOG_LEVELS[level] < LOG_LEVELS[config.level]) {
      return;
    }
    
    const formattedMessage = formatMessage(level, context, message, data);
    logToConsole(level, formattedMessage);
    logToUI(formattedMessage);
    
    // Return the formatted message for potential further use
    return formattedMessage;
  }

  // Public API
  return {
    // Configuration
    configure: function(options) {
      config = { ...config, ...options };
      this.debug('Logger', 'Logger configured', config);
    },
    
    // Enable/disable logging
    enable: function() {
      config.enabled = true;
      this.info('Logger', 'Logging enabled');
    },
    
    disable: function() {
      this.info('Logger', 'Logging disabled');
      config.enabled = false;
    },
    
    // Log level setters
    setLevel: function(level) {
      if (LOG_LEVELS[level] !== undefined) {
        config.level = level;
        this.info('Logger', `Log level set to ${level}`);
      }
    },
    
    // Logging methods
    debug: function(context, message, data) {
      return log('DEBUG', context, message, data);
    },
    
    info: function(context, message, data) {
      return log('INFO', context, message, data);
    },
    
    warn: function(context, message, data) {
      return log('WARN', context, message, data);
    },
    
    error: function(context, message, data) {
      return log('ERROR', context, message, data);
    },
    
    // Get current configuration
    getConfig: function() {
      return { ...config };
    }
  };
})();

// For Figma plugin environment
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Logger;
}
