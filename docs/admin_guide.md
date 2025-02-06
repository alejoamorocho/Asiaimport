# Administrator Guide

## System Architecture

### Components
1. **Backend (Django)**
   - REST API
   - Database management
   - Authentication
   - PDF generation
   - Task processing

2. **Frontend (React)**
   - User interface
   - State management
   - API integration

3. **Services**
   - PostgreSQL database
   - Redis for caching and task queue
   - Celery for async tasks

### Directory Structure
```
cosmedical-import/
├── backend/
│   ├── core/                 # Django project settings
│   └── inventory/            # Main application
│       ├── models/           # Database models
│       ├── api/              # API views and serializers
│       ├── tasks/            # Celery tasks
│       └── templates/        # PDF templates
├── frontend/
│   └── src/
│       ├── components/       # React components
│       ├── services/         # API services
│       └── store/           # State management
└── docker/                  # Docker configuration
```

## System Administration

### User Management

#### Creating Users
1. Access Django admin interface
2. Navigate to Users section
3. Click "Add User"
4. Set required fields:
   - Username
   - Password
   - Email
   - Permissions

#### Permission Groups
Predefined groups:
- **Administrators**: Full access
- **Managers**: Import and report access
- **Operators**: Basic product and import operations

To create new group:
1. Go to Groups in admin
2. Select permissions
3. Assign users

### Database Management

#### Backup
```bash
# Manual backup
docker-compose exec db pg_dump -U cosmedical_user cosmedical_db > backup.sql

# Automated backup (add to crontab)
0 2 * * * /path/to/backup-script.sh
```

#### Restore
```bash
# Stop services
docker-compose down

# Restore database
docker-compose exec db psql -U cosmedical_user cosmedical_db < backup.sql

# Restart services
docker-compose up -d
```

### File Storage

#### Media Files
- Location: `/app/media/`
- Subdirectories:
  - `pdfs/`: Generated PDFs
  - `documents/`: Import documents
  - `temp/`: Temporary files

#### Static Files
- Location: `/app/static/`
- Collected with: `python manage.py collectstatic`
- Served through Nginx in production

### Monitoring

#### Logs
- Application logs: `docker-compose logs backend`
- Celery logs: `docker-compose logs celery_worker`
- Nginx logs:
  - Access: `/var/log/nginx/access.log`
  - Error: `/var/log/nginx/error.log`

#### Performance Monitoring
1. Database:
   ```sql
   -- Check active connections
   SELECT * FROM pg_stat_activity;
   
   -- Table sizes
   SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
   FROM pg_catalog.pg_statio_user_tables
   ORDER BY pg_total_relation_size(relid) DESC;
   ```

2. Redis:
   ```bash
   redis-cli info
   ```

3. Celery:
   ```bash
   celery -A core inspect active
   celery -A core inspect reserved
   ```

### Security

#### SSL/TLS Configuration
1. Obtain certificate
2. Configure Nginx:
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       # Other SSL settings...
   }
   ```

#### Firewall Rules
```bash
# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow PostgreSQL (only from internal network)
ufw allow from 10.0.0.0/8 to any port 5432
```

#### Security Best Practices
1. Keep systems updated
2. Regular security audits
3. Monitor access logs
4. Implement rate limiting
5. Use strong passwords
6. Regular backup testing

### Maintenance Tasks

#### Regular Maintenance
1. Database optimization:
   ```sql
   VACUUM ANALYZE;
   ```

2. Clear old files:
   ```bash
   # Clear old PDFs (>30 days)
   find /app/media/pdfs -mtime +30 -delete
   ```

3. Monitor disk space:
   ```bash
   df -h
   du -sh /app/media/*
   ```

#### Troubleshooting

1. PDF Generation Issues:
   ```bash
   # Check Celery tasks
   celery -A core inspect active
   
   # Check logs
   docker-compose logs celery_worker
   ```

2. Database Issues:
   ```sql
   -- Check locks
   SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa
   ON pl.pid = psa.pid;
   ```

3. Performance Issues:
   ```sql
   -- Slow queries
   SELECT * FROM pg_stat_activity
   WHERE state = 'active' AND now() - query_start > interval '5 minutes';
   ```

### Scaling

#### Horizontal Scaling
1. Add more Celery workers:
   ```bash
   docker-compose up -d --scale celery_worker=3
   ```

2. Configure load balancing in Nginx:
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

#### Vertical Scaling
1. Increase resources in docker-compose.yml:
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

### Backup Strategy

#### Data to Backup
1. Database
2. Media files
3. Configuration files
4. SSL certificates

#### Backup Schedule
- Daily: Database dumps
- Weekly: Full system backup
- Monthly: Archive old data

#### Retention Policy
- Keep daily backups for 7 days
- Keep weekly backups for 1 month
- Keep monthly backups for 1 year

### Disaster Recovery

#### Recovery Steps
1. Restore latest backup
2. Verify data integrity
3. Update DNS if needed
4. Test system functionality

#### Recovery Time Objectives
- Database: < 1 hour
- File storage: < 2 hours
- Full system: < 4 hours
