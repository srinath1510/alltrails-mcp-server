# DEPRECATION NOTICE

## Project Status: DEPRECATED AND NON-FUNCTIONAL

**Date:** January 25, 2026  
**Status:** All functionality disabled  
**Reason:** Terms of Service violation

---

## What Happened?

On January 25, 2026, I received a message from James Graham, CTO of AllTrails, requesting that this repository be taken down or disabled due to violations of AllTrails' Terms of Service.

### Violations Cited

1. **Unauthorized scraping/data extraction** - The repository scraped AllTrails' website without permission, which is prohibited by their ToS
2. **Intellectual property violations** - AllTrails' content (trail descriptions, ratings, summaries) is protected by copyright
3. **Unauthorized redistribution** - Exposing AllTrails' data through a third-party interface without a license

### My Response

I have immediately:
- ✅ Disabled all scraping functionality in `app/alltrails_scraper.py`
- ✅ Modified `server.py` to exit immediately with a deprecation message
- ✅ Updated README.md with prominent deprecation warnings
- ✅ Maintained the repository structure to preserve GitHub stars and for historical/educational purposes

---

## Important Notes

### For Users
- **DO NOT USE THIS CODE** - It will not work and violates Terms of Service
- Use [AllTrails' official website](https://www.alltrails.com/) instead
- Contact AllTrails directly if you need API access

### For Developers
- **DO NOT FORK OR REPLICATE** this approach for AllTrails or any other website
- Always check a website's Terms of Service before scraping
- Respect intellectual property rights and copyright
- Use official APIs when available
- Get explicit written permission before scraping any website

### For the Community
This repository serves as an educational example of:
- ✅ How to properly respond to ToS violation requests
- ✅ The importance of reading and respecting Terms of Service
- ✅ Why you should use official APIs instead of scraping
- ❌ What NOT to do when building data extraction tools

---

## Lessons Learned

1. **Always read Terms of Service** before building tools that interact with websites
2. **Scraping is often prohibited** even if data appears "publicly available"
3. **Respect intellectual property** - just because you can access data doesn't mean you can redistribute it
4. **Use official APIs** when available, or contact the company for permission
5. **Be responsive** when companies reach out about violations

---

## Timeline

- **January 2026**: Project created and published
- **January 25, 2026**: Contacted by AllTrails CTO
- **January 25, 2026**: All functionality disabled, deprecation notices added

---

## Contact

If you have questions about this deprecation, please open an issue (not for requesting the code to be re-enabled).

For trail data access, contact AllTrails directly at their official website.

---

**Remember: Respect Terms of Service. Respect copyright. Build responsibly.**
