СУТЬ РАБОТЫ: ПРИ ПОДКЛЮЧЕНИИ КЛИЕНТА – ЕГО IP,ИМЯ,ID заносится в базу
Авторский пример по sourcepawn

#include <sourcemod> //обязательная библиотека
Handle g_SQL = INVALID_HANDLE;
bool MYSQL;
public OnPluginStart()
{
	if (!SQL_CheckConfig("section_name")) //проверка секции
	{
		SetFailState("Секция \"section_name\" не найдена в databases.cfg"); //отсутсвие секции с указанием на подключение к БД
		return;
	}

	char error[256];
	g_SQL = SQL_Connect("section_name", true, error, 256);
	if (g_SQL == INVALID_HANDLE)
	{
		LogError(error);
		SetFailState("Не удалось установить SQL соединение");
		return;
	}

	// тип соединения (mysql или sqlite)
	char driver[15]; 
	SQL_ReadDriver(g_SQL, driver, 15);
	MYSQL = StrEqual(driver, "mysql", false);
	LogMessage("Установлено %s соединение", MYSQL ? "MYSQL" : "SQLite"); //логгирование вывода результата подключения к базе

	// создаем таблицу
	if (!MYSQL) SQL_TQuery(g_SQL, SQL_DefCallback, "CREATE TABLE IF NOT EXISTS `my_table` (steamid INTEGER PRIMARY KEY, ip INTEGER, name TEXT)", 0); //создание таблицы если SQL
	else SQL_TQuery(g_SQL, SQL_DefCallback, "CREATE TABLE IF NOT EXISTS `my_table` (`steamid` int(3) NOT NULL,`ip` int(20) NOT NULL, `name` varchar(32) NOT NULL, PRIMARY KEY (`steamid`))", 0); //создание таблицы если MYSQL
}
 
public SQL_DefCallback(Handle owner, Handle hndl, const char error[], any Data)
{
    if (hndl == INVALID_HANDLE) LogError(error); //вывод ошибки при отсутствии подключения
}

public void OnClientConnect(int client)
{
	char name[32],char buffer[1024]; //создание буфферов временных данных
	int steamid;
	if(client && !IsFakeClient(client)) //проверка валидности клиента
	{
		if(g_SQL != INVALID_HANDLE)
		{
			GetClientIP(client, char[] ip, sizeof(ip),true); //получение ip клиента в строку "ip"
			GetClientName(client, name, sizeof(name)); //получение имени клиента в строку "name"
			steamid = GetClientUserId(client); // получения id клиента в переменную "steamid"
			Format(buffer,sizeof(buffer), "INSERT INTO `my_tab` (`steamid`,`ip`,`name`)VALUES(`%s`,`%s`,`%s`)",steamid,ip,name); //форматирование строки для удобства
			SQL_TQuery(g_SQL, SQL_DefCallback, buffer, 0); //выполнение запроса
		}
	}
}



