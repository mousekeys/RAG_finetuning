# Security Policy

## Supported Versions

This is an initial release. Security updates will be applied to the latest version.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Considerations

### Backend Security

1. **API Security**
   - The backend API currently has CORS set to allow all origins (`allow_origins=["*"]`)
   - **Production Recommendation**: Update CORS to specify your Android app's origin only
   - Consider implementing authentication (JWT, OAuth2) for production use

2. **Network Security**
   - The backend uses HTTP by default
   - **Production Recommendation**: Deploy with HTTPS/TLS encryption
   - Use environment variables for sensitive configuration

3. **Input Validation**
   - All API inputs are validated using Pydantic models
   - Additional sanitization may be needed for production use

4. **Dependencies**
   - All dependencies have been checked against the GitHub Advisory Database
   - Known vulnerabilities have been patched
   - Regular dependency updates are recommended

### Android App Security

1. **Network Communication**
   - The app uses cleartext traffic for local development
   - **Production Recommendation**: Remove `android:usesCleartextTraffic="true"` and use HTTPS only
   - Implement certificate pinning for enhanced security

2. **Data Storage**
   - Currently, no sensitive data is stored on the device
   - If implementing data persistence, use Android's EncryptedSharedPreferences

3. **API Credentials**
   - If implementing authentication, use Android Keystore for secure credential storage
   - Never hardcode API keys or secrets in the app

### Data Privacy

1. **Financial Data**
   - Financial documents are stored in ChromaDB vector database
   - Data persists locally in the `chroma_db` folder
   - No encryption at rest is implemented by default
   - **Recommendation**: Implement encryption for sensitive financial data

2. **Logging**
   - Debug logging is enabled in the Android app
   - **Production Recommendation**: Disable debug logging and ensure no sensitive data is logged

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do Not** open a public issue
2. Email the maintainers directly with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

3. Allow reasonable time for a fix to be developed and released
4. Coordinate disclosure timing with the maintainers

## Security Best Practices for Deployment

### Backend Deployment

1. **Use Environment Variables**
   ```python
   # Example: Use environment variables for configuration
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   API_KEY = os.getenv("API_KEY")
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

2. **Implement Rate Limiting**
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

3. **Add Authentication**
   ```python
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   @app.post("/documents/add")
   async def add_document(doc: DocumentInput, credentials = Depends(security)):
       # Verify credentials
       ...
   ```

4. **Use HTTPS**
   - Deploy behind a reverse proxy (nginx, Apache)
   - Use Let's Encrypt for free SSL certificates
   - Configure HTTPS in your deployment

### Android App Deployment

1. **Network Security Configuration**
   Create `res/xml/network_security_config.xml`:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <network-security-config>
       <domain-config>
           <domain includeSubdomains="true">your-api-domain.com</domain>
           <pin-set>
               <pin digest="SHA-256">YOUR_CERTIFICATE_HASH</pin>
           </pin-set>
       </domain-config>
   </network-security-config>
   ```

2. **ProGuard/R8 Configuration**
   - Enable code obfuscation for release builds
   - Protect API keys and sensitive strings

3. **Secure API Communication**
   ```kotlin
   // Use secure configuration for production
   private const val BASE_URL = BuildConfig.API_URL  // From build config
   ```

## Regular Security Maintenance

1. **Update Dependencies**
   ```bash
   # Python
   pip list --outdated
   pip install --upgrade -r requirements.txt
   
   # Android
   # Check for updates in Android Studio
   ```

2. **Run Security Scans**
   ```bash
   # Python security scanning
   pip install safety
   safety check
   
   # Or use bandit for code analysis
   pip install bandit
   bandit -r .
   ```

3. **Code Review**
   - Review all code changes for security implications
   - Use automated security scanning tools
   - Follow secure coding guidelines

## Known Limitations

1. **Local LLM Integration**
   - The template for Ollama integration makes HTTP requests to localhost
   - Ensure Ollama is properly secured if exposed to network

2. **Vector Database**
   - ChromaDB stores data in plaintext
   - Consider implementing encryption layer for sensitive data

3. **No User Authentication**
   - Current implementation has no user authentication
   - Add authentication before deploying to production

## Security Checklist for Production

- [ ] Update CORS policy to specific origins
- [ ] Implement user authentication and authorization
- [ ] Use HTTPS/TLS for all communication
- [ ] Remove cleartext traffic allowance from Android app
- [ ] Implement certificate pinning
- [ ] Enable rate limiting on API endpoints
- [ ] Add input sanitization beyond basic validation
- [ ] Implement database encryption
- [ ] Disable debug logging
- [ ] Review and update security policies
- [ ] Implement proper error handling (don't expose stack traces)
- [ ] Add security headers (HSTS, CSP, etc.)
- [ ] Regular dependency updates
- [ ] Security audit and penetration testing

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [OWASP Mobile Security](https://owasp.org/www-project-mobile-top-10/)
