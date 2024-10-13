def obtener_resumen(df, fecha_inicio, fecha_final):
    # Verificar si el DataFrame está vacío
    if df.empty:
        resumen = {
            'Total Ingresos': 'sin historial',
            'Promedio de Ingresos': 'sin historial',
            'Varianza de Ingresos': 'sin historial',
            'Desviacion Estandar de Ingresos': 'sin historial',
            'Total Gastos': 'sin historial',
            'Promedio de Gastos': 'sin historial',
            'Varianza de Gastos': 'sin historial',
            'Desviacion Estandar de Gastos': 'sin historial',
            'Ratio Ingresos-Gastos': 'sin historial',
            'Total Transacciones': 'sin historial',
            'Promedio de Saldo en Cuenta': 'sin historial'
        }
        return resumen
    
    # Filtrar los datos por el rango de fechas y por número de cuenta
    df_periodo = df[(df['Fecha de Transaccion'] >= fecha_inicio) & 
                    (df['Fecha de Transaccion'] <= fecha_final)]
    
    # Calcular las sumas y promedios
    resumen = {
        # Ingresos
        'Total Ingresos': df_periodo['Monto de Ingresos'].sum(),
        'Promedio de Ingresos': df_periodo['Monto de Ingresos'].mean(),
        'Varianza de Ingresos': df_periodo['Monto de Ingresos'].var(),
        'Desviacion Estandar de Ingresos': df_periodo['Monto de Ingresos'].std(),
        # Gastos
        'Total Gastos': df_periodo['Monto de Gastos'].sum(),
        'Promedio de Gastos': df_periodo['Monto de Gastos'].mean(),
        'Varianza de Gastos': df_periodo['Monto de Gastos'].var(),
        'Desviacion Estandar de Gastos': df_periodo['Monto de Gastos'].std(),
        # Ratio
        'Ratio Ingresos-Gastos': df_periodo['Monto de Ingresos'].sum() / df_periodo['Monto de Gastos'].sum() if df_periodo['Monto de Gastos'].sum() != 0 else 'sin historial',
        # Transacciones
        'Total Transacciones': df_periodo['Cantidad de Transacciones'].sum(),
        # Saldo en cuenta
        'Promedio de Saldo en Cuenta': df_periodo['Saldo Total en Cuenta'].mean()
    }
    
    return resumen