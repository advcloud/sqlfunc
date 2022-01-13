CREATE PROCEDURE [dbo].[iotdata1]
  @iotdata nvarchar(30) = NULL
AS
BEGIN
  SELECT *
  FROM home_stat_temp
  WHERE temperature = ISNULL(@iotdata,temperature)
  FOR JSON PATH
END