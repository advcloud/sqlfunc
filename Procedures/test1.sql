CREATE PROCEDURE [dbo].[plugname1]
  @plugname nvarchar(30) = NULL
AS
BEGIN
  SELECT *
  FROM cablels
  WHERE Item_Number = ISNULL(@plugname,Item_Number)
  FOR JSON PATH
END