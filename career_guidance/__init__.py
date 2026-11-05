# PyMySQL is pure Python, so it installs on Vercel without native MySQL client headers.
import pymysql

pymysql.install_as_MySQLdb()
