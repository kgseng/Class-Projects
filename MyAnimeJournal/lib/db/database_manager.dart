import 'package:flutter/services.dart';
import 'package:journal/views/new_journal_entry.dart';
import 'package:sqflite/sqflite.dart';
import 'dart:async';

class DatabaseManager {
  static const String DATABASE_FILENAME = 'journal.db';
  static const String SQL_CREATE_SCHEMA = "assets/schema_1.sql.txt";
  static const String SQL_INSERT =
      'INSERT INTO journal_entries(title, body, rating, date) VALUES(?, ?, ?, ?)';
  static const SQL_SELECT = 'SELECT * FROM journal_entries';

  static Future<String> getSchema() async {
    return await rootBundle.loadString(SQL_CREATE_SCHEMA);
  }

  static late DatabaseManager _instance;
  final Database db;
  DatabaseManager._({required Database database}) : db = database;

  factory DatabaseManager.getInstance() {
    assert(_instance != null);
    return _instance;
  }

  static Future initialize() async {
    String dbSchema = await getSchema();
    final db = await openDatabase(DATABASE_FILENAME, version: 1,
      onCreate: (Database db, int version) async {
      createTables(db, dbSchema);
    });
    _instance = DatabaseManager._(database: db);
  }

  static void createTables(Database db, String sql) async {
    await db.execute(sql);
  }

  void saveJournalEntry({required AnimeFields dto}) {
    db.transaction((txn) async {
      await txn
          .rawInsert(SQL_INSERT, [dto.title, dto.review, dto.rating, dto.date]);
    });
  }

  Future<List<Map>> journalEntries() {
    return db.rawQuery(SQL_SELECT);
  }
}
